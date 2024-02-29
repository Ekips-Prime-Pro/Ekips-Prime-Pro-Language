# Spike Custom Programming Language and Compiler

## Introduction

Welcome to the documentation for Spike Custom System Programming! This guide will provide you with all the information you need to get started with programming in Spike Custom System Programming.

## Table of Contents

- [Installation](#installation)
- [Syntax](#syntax)
- [Functions](#functions)
- [Examples](#examples)

## Installation

To use the Spike Custom System Programming LAnguage, you need to install the compiler and runtime environment. Follow the instructions below to get started:

1. Download the latest version of the Spike Custom System Programming Language compiler from the official website.
2. Install the compiler on your system by running the installer.
3. Verify the installation by opening a terminal and running the programm in cli mode command.

## Syntax

The Spike Custom System Programming Language has a simple and intuitive syntax that is easy to read and write. Here are some key features of the syntax:

- After every Function you have to place a semicolon (`;`).
- The curly brackets define function uneque variables like `wait{1}` (`{}`).
- If you want to have to varables in curly brackets you have to add an colon (`:`)
- Comments can be added using the `//` or `/* */` syntax.

## Functions

The main functions of the Spike Custom System Programming Language are for the basic use of the Spike Prime Custom Operating System and programming with ai enforced functions.
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

The best way to learn the language you have to remeber the syntax and the functions but then you have to practice. The following code examples will show you how to begin after you have try'd it you can open the Examples.md file and learn more about the Spike Custom System Programming Language.

1. `drive{10};` or `ai.drive{10};`
2. `module{100};` or `ai.module{100};`
3. `parallel{ai.drive{10}:module{100}};`
4. `sensor{color};`
5. `ai_train_data_save{data_file};` or `ai_train_data_load{data_file};` or `ai_model_chose{supervised_learning};`
6. `print{Hello World};`
7. `calibrate{10};` this will define the distance that will be driven.
8. `tank{90:30};`