#! /usr/bin/env python
# encoding: utf-8
from invoke import Collection, Program
from tasker import tasks

program = Program(namespace=Collection.from_module(tasks), version='0.1.0')