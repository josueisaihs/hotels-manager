# Tech Assessment

## Table of Contents

- [The Problem](#the-problem)
- [The Solution](#the-solution)
- [The Deliverable](#the-deliverable)
- The Resolution
  - [Task 1](/docs/task1.md)
  - [Task 1.1](/docs/task1.1.md)
  - [Task 2](/docs/task2.md)

## The Problem

Our content team is having problems manually managing thousands of hotels and hotel chains
that are stored in our database and want an API to automate some of their tasks.

As a first step, they've requested an API to manage hotels and an admin section for both hotels and
chains.

We've started a new Django project to build a Django Admin and API that will allow them to manage
the hotel data better. Unfortunately, the developer that was working on the project is on sick
leave and has left the code incomplete.

## The Solution

### Task 1

Start the project, fix it, apply good practices to leave it as if it were yours, and solve as much
technical debt as possible. Also, we would like to have the API documented.
The hotel API create view need some special attention.

### Task 2

You are in a refinement session with the Backend team and the Product Owner. Now that the hotel API
is finished they want to request a new feature.

The content team wants to be able to edit the hotels that are in the database through an API
endpoint but with the following requirements:

- Staff users can change hotel information without restrictions.
- Non-staff users can submit changes, but they won't be applied immediately.
  The changes will be stored so a staff user can review them in the admin and decide whether to apply them or not.
  - The review admin section should contain the old and new values and buttons to accept or reject.
  - An email should be sent to a reviewer to notify that there is a new submission to review.
- This API could be used to add new content from external parties and we could get thousands of requests. Make sure your solution scales.

Think of it as a real refinement session where you could ask questions to anyone in the meeting,
but assume anything you need not to get blocked.

Your job is to provide a list of tasks and for each one of them a technical solution. Describe in
detail the changes that need to be done in the project (endpoints, models, admin, tasks, etc) with
links to the code if needed for better explanations. Take into account that this new feature
can be implemented by another developer, and it could be done several weeks in the future.

## The Deliverable

Create a Pull Request against this repo with all the fixes and changes needed for Task #1 and the
solution to Task #2 (could be a new section at the Readme, a separate document, etc). Use as many commits as you want.
