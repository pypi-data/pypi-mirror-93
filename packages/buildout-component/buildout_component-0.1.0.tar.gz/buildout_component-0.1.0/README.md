# buildout-component

Python Buildout component tool, a tool program used to help componentize the settings of zc.buildout.

## Introduction

Buildout is a great tool for Python development and deployment environment, but it requires a lot of settings to work
well.

I am used to Buildout each reusable item as a component. If there is a component that needs to be reused, just copy its
content to a new project to use it directly, but it still depends on manual settings and configuration.

In order to simplify the complicated settings, I wrote a gadget called `buildout-component` to help me set up the
componentized environment of Buildout more conveniently.

## Features

- Generate the file structure of Buildout Component;
- Through the question and answer method, to generate the Buildout profile.

## Installation

Install `buildout-component`:

    $ pip install buildout-component

## Use

After installation, you can execute the `buildout-component` command:

- set up

        $ buildout-component setup

- Display set value

        $ buildout-component show-options

- Create Component

        $ buildout-component create