import argparse
import github
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload assets to a GitHub release")
    parser.add_argument(
        "--secret_env",
        help="Name of env variable with the access token",
        default="SECRET_TOKEN",
    )
    parser.add_argument("--repo", help="Repository name", required=True)
    parser.add_argument("--tag", help="Release tag", required=True)
    parser.add_argument("files", help="Files to upload", nargs="*")
    args = parser.parse_args()

    if args.secret_env not in os.environ:
        print(f"{args.secret_env} not found in environment, skipping upload")
        exit()

    secret = os.environ.get(args.secret_env)
    git = github.Github(secret)
    user = git.get_user()
    repo = user.get_repo(args.repo)
    release = repo.get_release(args.tag)
    for file in args.files:
        release.upload_asset(file)
