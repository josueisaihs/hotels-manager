# [Task 1](/docs/task1.md#table-of-contents) / TASK 1 - Solution 2

TAG `task1.1`

## Description

This is a refactoring of the previous implementation, and this document shows the changes. The main reason for the refactoring is to improve code readability and project scalability, as well as applying the DRY principle by avoiding the need to repeat hotel chain names in a configuration variable.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Settings](#settings)
  - [Configuration Variables](#configuration-variables)
- [Components](#components)
  - [Signals](#signals)
  - [Managers](#managers)
- [Business Logic](#business-logic)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Settings

### Configuration Variables

This variable is no longer used, instead a field is used in the `HotelChain` model called `auto_assign` which is a boolean that indicates whether a chain should be automatically assigned to a hotel.

- `SPECIAL_CHAINS` ![DEPRECATED](https://img.shields.io/badge/-DEPRECATED-red)

## Components

### Signals

Signal handlers have been defined for the API models:

- `hotel_signal_pre_save`: Signal to auto-assign a hotel chain to a hotel
- `hotel_signal_post_save`: Signal to relate hotels according to the business logic and send an email notification
- `hotel_chain_signal_pre_save`: Signal to format the title of the hotel chain before saving it

### Managers

Mangers have been defined for the API models:

- `HotelManager`: Manager for the `Hotel` model
  - `nested_create`: Method to create hotels with nested hotel chains.

- `HotelChainManager`: Manager for the `HotelChain` model
  - `create`: Method to create a hotel chain and keep the `title` field unique.
  - `filter_by_title_with_auto_assign`: Method to filter hotel chains by title and assign a hotel to the chain if it exists.

## Business Logic

The business logic of the API is as follows:

- A hotel can belong to a single hotel chain or not belong to any hotel chain.
- If a hotel chain is marked as auto_assign, when a hotel is created a logic will be applied:
  - the title of the chain is contained in the name of the hotel
  - the title of the string is more than 3 characters
  - the hotel does not have an assigned chain
- When a hotel is created if it has a chain assigned, it will be notified by email if it has an email for it.
- A hotel is related to other hotels if they belong to the same chain.
- A hotel is related to other hotels if they belong to the same chain.
- A hotel chain is created if its title is unique; otherwise, the existing hotel chain is returned.
- The title of a hotel chain is formatted as "title" before saving. Example: "hotel chain", "HoTel ChAiN" -> "Hotel chain"

<!--
Notes

Comment `# region NAME` is used to group the code into sections and facilitate reading the code. To collapse the sections, you must install the `Better Comments` extension in Visual Studio Code. And also marks the region on the editor minimap.

Comment `# type: ignore` is used to ignore typing errors in the code.
-->
