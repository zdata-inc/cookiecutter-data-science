Inspired by coming up with a solution to [[DVC]] warts, I've started playing around with git-annex to see if it is applicable to our use cases. Below is a walkthrough.
## Installation of the tools

The first step is to install the various prerequisite tools. The install instructions below assume you're using a mac. If not, just go to the websites of the respective tools and follow their platform-specific instructions.

1. git annex
	1. `brew install git-annex`
2. rclone
	- `brew install rclone`
3. gnupg.
	- This is not strictly a requirement, but if you get an error like `git-annex: gpg: createProcess: posix_spawnp: does not exist (No such file or directory)` when running `git annex initremote` using the `git-annex-remote-rclone` plugin then a fresh install of GPG will fix it.
	- `brew install gnupg` 
4. git annex rclone script
	- Clone this repo: https://github.com/git-annex-remote-rclone/git-annex-remote-rclone. Check out the latest released version (e.g. `git checkout v0.8`). Then add the directory to your `$PATH`.

## Initial Setup of a repo

Start by setting up the git repository in our usual centralized way, with a repo hosted on github and local clones. I won't share explicit commands for this, but from here on in the walkthrough I assume there is a repo hosted on github that two people on two different machines have cloned locally into directories `repo_a` and `repo_b` respectively. 

User A runs `git annex init` in `repo_a` and then `git annex push` . The output shows that some stuff is pushed to github, but it will also say something along the lines of `Remote origin not usable by git-annex; setting annex-ignore`. This is because git annex realizes that the github remote is a bare repository and can't be used to actually store the data. Similarly, in `repo_b` a `git annex pull` will pull those branches git annex has made, but it will give a similar message. Git annex stores its information in branches in the git repo that we don't directly touch and are distinct from our branches.

Now we need a place to store the data.
## Initial setup of a GCS special remote

One person, let's say person A, goes onto the GCS console and creates a bucket, which we'll call `annexgcs`. They should then give fine-grained access to principals via GCS.

Then setting up the remote in rclone they run `rclone config` and create a new remote, which we'll call `rcloneremote`.  rclone will ask you a bunch of questions and the only ones you don't need to just use the default for are:
- Storage. This should be GCS (option 16).
- project_number. This should be the project number for the Google Cloud project that houses the bucket.
- bucket_policy_only set to true.
The rest you can just hit 'enter' for unless there's a specific reason it should be changed.

Now we need git annex to connect to this rclone remote. This can be achieved with:

```
git annex initremote gcs type=external externaltype=rclone target=rcloneremote prefix=annexgcs chunk=50MiB encryption=shared mac=HMACSHA512 rclone_layout=lower
```
Here `gcs` is the name of the remote we're assigning within git-annex, while `rcloneremote` is the name of the remote already existing in rclone, and `annexgcs` is the bucket name on GCS.

`repo_a` can now `git annex push` and this information will be pushed up to github. `repo_b` can `git annex pull` to get the details in git annex about the remote. However, the rclone remote presumably that needs to be set up on the other machine so person B should:
- Set up an appropriately named remote in rclone as per the instructions for rclone above.
- Then enable said remote in git annex with `git annex enableremote gcs`. Here git annex is using the remote name gcs established in `repo_b` and then pushed to github.
## Managing data

Ok, we're now set with our git remote and GCS special remote for storing the data. What does our data management workflow look like?

Suppose there's a directory of images in `repo_x` called `images/` . Let's commit this and share it with the others

```
git annex add images/
```

This will add the objects to git annex and stage in git the addition of some symlinks in `images/` that point to said objects. Now we:

```
git commit -m 'added images'
```

We push our git commit to github and our data to GCS simultaneously using:

```
git annex push -J10
```
The -J10 says to parallelize over 10 jobs. This value can be higher or lower, but I've found including it is important for pushing lots of small files, in the same way you may have found the `-m` flag really important when using `gsutil -m cp -r`.

Now in `repo_y` we run:
```
git annex pull -J10 
```
to get the data.

Note that `git annex add` is only run once to start git annex tracking a file. If you want to remove, or change files, follow the instructions in the [git-annex walkthrough](https://git-annex.branchable.com/walkthrough/). Just note however that we won't be using the `git annex sync` commands that you might see in the git annex documentation. That seems to be for a somewhat different use case. It's best for us to push and pull as per a typical git workflow.

Note that modifying files requires making them unlocked with `git annex unlock` See more details [here](https://git-annex.branchable.com/tips/unlocked_files/).

