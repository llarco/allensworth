load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "io_bazel_rules_python",
    commit = "fdbb17a4118a1728d19e638a5291b4c4266ea5b8",
    remote = "https://github.com/bazelbuild/rules_python.git",
)

load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()

load("@io_bazel_rules_python//python:pip.bzl", "pip_import")

pip_import(
    name = "pip_deps",
    requirements = "//:requirements.txt",
)

load("@pip_deps//:requirements.bzl", "pip_install")

pip_install()
