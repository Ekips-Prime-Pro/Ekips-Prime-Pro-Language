# My Programming Language

## Introduction

Welcome to the documentation for My Programming Language! This guide will provide you with all the information you need to get started with programming in My Programming Language.

## Table of Contents

- [Installation](#installation)
- [Syntax](#syntax)
- [Functions](#functions)
- [Examples](#examples)

## Installation

To use the Spike custom Programming Language, you need to install the compiler and runtime environment. Follow the instructions below to get started:

1. Download the latest version of the My Programming Language compiler from the official website.
2. Install the compiler on your system by running the installer.
3. Verify the installation by opening a terminal and running the `mypl --version` command.

## Syntax

The Spike custom  Programming Language has a simple and intuitive syntax that is easy to read and write. Here are some key features of the syntax:

- After every Function you have to place a semicolon (`;`).
- The curly brackets define function uneque variables like `wait{1}` (`{}`).
- If you want to run two functions in parallel you have to add an colon (`:`)
- Comments can be added using the `//` or `/* */` syntax.

## Functions

The main functions of the Programming Language are for the basic use of the Spike Prime Custom Operating System and programming with ai enforced functions.
There are four build in functions.

- The `Drive` function is for driving a motorpair forward and backward.
- The `Tank` function is for making turns.
- The `Module` function is for controling a single motor.
- The `Calibration` function is for calibrating the robot and it motors, it also enhances the ai's capabilities.
- The `AI` function is for controling the artificial inteligence which is build in for every module if there are datasets to build from, for this there will be an extra Guide.
- The `Sensor` function is for controling the Input for the artificial inteligence.
- The `Parallel` function will run multible thing simultanius.
- The `Wait` function will hold the programm for a few moments.
- The `print` function will print any value you give it.

## Examples

1. `drive{10};` or `ai.drive{10};`
2. `module{100};` or `ai.module{100};`
3. `parallel{ai.drive{10}:module{100}};`
4. `sensor{color};`
5. `ai_train_data_save{data_file};` or `ai_train_data_load{data_file};` or `ai_model_chose{supervised_learning}`
