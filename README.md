# PurePage

[English](README.md) | [Chinese](README_CN.md)

PurePage is a minimalist blog page, entirely based on FastHTML, and can use built-in Markdown to render article content. It supports rendering mathematical formulas, allowing you to focus on writing without worrying about complex blog system setup and maintenance. PurePage emphasizes localization and data autonomy, ensuring your content is always under your control.

I developed PurePage because I have tried many different blogging systems, such as Hexo, Docusaurus 2, and Notion, but always felt they were too complex and difficult to use. Recently, FastHTML came out, allowing me to develop websites by writing only Python code. Therefore, I thought of using FastHTML to create a simple blog page to make writing easier.

The features of PurePage are very simple, with no unnecessary settings or complex functions, only a simple search function and an automatically generated article list. At the same time, PurePage's rendering effect is very good, making your articles look more beautiful and professional.

If you are a minimalist blogger looking for a simple and efficient blog page that emphasizes data autonomy and localization, then PurePage is definitely a good choice. You are welcome to try it out and provide feedback and suggestions.

## ✨ Features

- The front-end and back-end are entirely written in Python, with the front-end implemented using FastHTML and tailwind.css

- markdown rendering

- Adaptive Interface

## User Guide

Run `scripts/Deploy.py` to generate the homepage directory

```bash
python scripts/Deploy.py
```

Get custom style list

```bash
python test/te_re.py
```

Generate custom style

```bash
npx tailwindcss -o ./static/tailwind.css --config tailwind.config.js
```