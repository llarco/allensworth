load("@pip_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

load(
    "@io_bazel_rules_python//python:python.bzl",
    "py_library",
    "py_test",
)

py_library(
    name = "power_supply",
    srcs = ["power_supply.py"],
    deps = [
        requirement("pyserial"),
    ]
)

py_test(
    name = "power_supply_test",
    srcs = ["power_supply_test.py"],
    deps = [":power_supply"],
)
