package(default_visibility = ["//visibility:public"])

load(
    "@io_bazel_rules_python//python:python.bzl",
    "py_binary",
)

py_binary(
    name = "publisher",
    srcs = ["publisher.py"],
    main = "publisher.py",
    deps = ["//power_supply"],
)

py_test(
    name = "publisher_test",
    srcs = ["publisher_test.py"],
    deps = [
        ":publisher",
        "//power_supply",
    ],
)
