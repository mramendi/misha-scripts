pushd /home/mramendi/repos/openshift-docs
git checkout $1 || git checkout --track upstream/$1 || exit 1
git pull upstream $1 || exit 1
git checkout -b RHDEVDOCS-6426-$1 || exit 1
grep --include=\*.adoc -r -l -e "making-open-source-more-inclusive.adoc" | xargs -L 1 ~/repos/misha-scripts/deinclude/editfile.sh
git status
echo "Enter to proceed with pull request, Ctrl-C to stop"
read
git commit -a -m "RHDEVDOCS 6426 Remove language note" | exit 1
git push -u mramendi RHDEVDOCS-6426-$1 | exit 1
gh pr create --base $1 --head mramendi:RHDEVDOCS-6426-$1 --title "RHDEVDOCS 6426 Remove language note - pipelines-docs-main" --body-file ../misha-scripts/deinclude/comment.txt
popd
