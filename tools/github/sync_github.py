from pathlib import Path
import subprocess

import yaml
from github import Github, Auth
from github.GithubException import GithubException

import time

# ----------------------------------------------------------------------
# Console Colors
# ----------------------------------------------------------------------

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# ----------------------------------------------------------------------
# Stats
# ----------------------------------------------------------------------

stats = {
    "labels_created": 0,
    "labels_existing": 0,

    "milestones_created": 0,
    "milestones_existing": 0,

    "issues_created": 0,
    "issues_updated": 0,
    "issues_unchanged": 0,
}

# ----------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------

BASE_DIR = Path(__file__).parent

ISSUE_DIR = BASE_DIR / "issues"
LABEL_FILE = BASE_DIR / "labels.yaml"
MILESTONE_FILE = BASE_DIR / "milestones.yaml"

# ----------------------------------------------------------------------
# GitHub
# ----------------------------------------------------------------------

def get_github():
    """Return an authenticated GitHub client using the GitHub CLI."""
    token = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    return Github(auth=Auth.Token(token))


def get_repo():
    """Return the HouseCall repository."""
    github = get_github()
    return github.get_repo("ajr32/housecall")


# ----------------------------------------------------------------------
# Loaders
# ----------------------------------------------------------------------

def load_labels():
    """Load labels from labels.yaml."""
    with open(LABEL_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["labels"]


def load_milestones():
    """Load milestones from milestones.yaml."""
    with open(MILESTONE_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["milestones"]


def load_issue(file):
    """Load an issue YAML file."""
    with open(file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ----------------------------------------------------------------------
# GitHub Synchronization
# ----------------------------------------------------------------------

def ensure_label(repo, name, color, description):
    """Create a label if it doesn't already exist."""
    try:
        repo.create_label(name=name, color=color, description=description)
        stats["labels_created"] += 1
        print(f"{GREEN}✓ Created label:{RESET} {name}")
    except GithubException as ex:
        if ex.status == 422:
            stats["labels_existing"] += 1
            print(f"{RED}• Label already exists:{RESET} {name}")
        else:
            raise


def ensure_milestone(repo, title, description):
    """Create a milestone if it doesn't already exist."""
    for milestone in repo.get_milestones(state="all"):
        if milestone.title == title:
            stats["milestones_existing"] += 1
            print(f"{RED}• Milestone already exists:{RESET} {title}")
            return milestone

    milestone = repo.create_milestone(title=title, description=description)
    stats["milestones_created"] += 1
    print(f"{GREEN}✓ Created milestone:{RESET} {title}")
    return milestone


def ensure_issue(
    repo,
    issue,
    issues,
    milestones,
    labels
):
    """Create an issue if it doesn't already exist."""

    title = issue["title"]

    milestone_obj = None

    if issue.get("milestone"):
        milestone_obj = milestones.get(issue["milestone"])

        if milestone_obj is None:
            print(
                f"{YELLOW}⚠ Milestone not found:{RESET} "
                f"{issue['milestone']}"
            )

    label_objects = []

    for label_name in issue.get("labels", []):
        label = labels.get(label_name)

        if label is None:
            print(f"{YELLOW}⚠ Label not found:{RESET} {label_name}")
            continue

        label_objects.append(label)

    existing = issues.get(title)

    if existing:

        changes = []

        # ----------------------------------------------------------
        # Compare body
        # ----------------------------------------------------------

        if existing.body != issue["body"]:
            changes.append("Body")

        # ----------------------------------------------------------
        # Compare milestone
        # ----------------------------------------------------------

        existing_milestone = (
            existing.milestone.title
            if existing.milestone
            else None
        )

        new_milestone = issue.get("milestone")

        if existing_milestone != new_milestone:
            changes.append("Milestone")

        # ----------------------------------------------------------
        # Compare labels
        # ----------------------------------------------------------

        existing_labels = sorted(
            label.name
            for label in existing.labels
        )

        new_labels = sorted(
            issue.get("labels", [])
        )

        if existing_labels != new_labels:
            changes.append("Labels")

        # ----------------------------------------------------------
        # Update if necessary
        # ----------------------------------------------------------

        if changes:

            existing.edit(
                body=issue["body"],
                milestone=milestone_obj,
                labels=issue.get("labels", [])
            )

            print(
                f"{GREEN}✓ Updated issue:{RESET} "
                f"{title} ({', '.join(changes)})"
            )
        else:

            stats["issues_unchanged"] += 1
            print(f"{RED}• Issue unchanged:{RESET} {title}")
        return

    repo.create_issue(
        title=title,
        body=issue["body"],
        milestone=milestone_obj,
        labels=label_objects
    )

    stats["issues_created"] += 1
    print(f"{GREEN}✓ Created issue:{RESET} {title}")

def sync_labels(repo):
    """Synchronize labels from labels.yaml."""
    labels = load_labels()
    print(f"\n{BLUE}Synchronizing {len(labels)} labels...{RESET}\n")
    for label in labels:
        ensure_label(repo, label["name"], label["color"], label["description"])


def sync_milestones(repo):
    """Synchronize milestones from milestones.yaml."""
    milestones = load_milestones()
    print(f"\n{BLUE}Synchronizing {len(milestones)} milestones...{RESET}\n")
    for milestone in milestones:
        ensure_milestone(repo, milestone["title"], milestone.get("description", ""))


def sync_issues(
    repo,
    issues,
    milestones,
    labels
):
    """Synchronize issues from the issues folder."""
    issue_files = sorted(ISSUE_DIR.rglob("*.yaml"))
    print(f"\n{BLUE}Synchronizing {len(issue_files)} issues...{RESET}\n")
    for file in issue_files:
        issue = load_issue(file)
        ensure_issue(
            repo,
            issue,
            issues,
            milestones,
            labels
        )

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

start = time.perf_counter()

def main():
    print(f"\n{BLUE}HouseCall GitHub Sync{RESET}")
    print("=" * 50)

    repo = get_repo()
    issues = {
        issue.title: issue
        for issue in repo.get_issues(state="all")
    }

    milestones = {
        milestone.title: milestone
        for milestone in repo.get_milestones(state="all")
    }

    labels = {
        label.name: label
        for label in repo.get_labels()
    }

    print(f"Repository: {repo.full_name}")

    sync_labels(repo)
    sync_milestones(repo)
    sync_issues(
        repo,
        issues,
        milestones,
        labels
    )

    print("\n" + "=" * 50)

    print("\nLabels")
    print("------")
    print(f"Created : {stats['labels_created']}")
    print(f"Existing: {stats['labels_existing']}")

    print("\nMilestones")
    print("----------")
    print(f"Created : {stats['milestones_created']}")
    print(f"Existing: {stats['milestones_existing']}")

    print("\nIssues")
    print("------")
    print(f"Created   : {stats['issues_created']}")
    print(f"Updated   : {stats['issues_updated']}")
    print(f"Unchanged : {stats['issues_unchanged']}")

    print(f"\n{GREEN}Synchronization complete!{RESET}")

if __name__ == "__main__":
    main()

elapsed = time.perf_counter() - start

print(f"\nCompleted in {elapsed:.2f} seconds.")