---
title: Health Care Application
date_added: 2016-06-30 00:00:00 -0500
vetsdotgov_url: https://www.vets.gov/healthcare/apply/
status: new
category: Apply
description: Making it easy to apply for VA health care online
tiles:

  - name: User Experience
    layout: image-compare
    before: old-healthcare.jpg
    after: healthcare.jpg

  - name: Daily Submissions
    layout: basic
    datapoint: 750
    context: on average

  - name: Automated processing
    layout: compare
    datapoint: 50%
    before: 4%
    context: of applications can now be processed automatically

  - name: Veteran testimonial
    layout: quote
    text: The other website takes you around the corner, over the meadow, and...in a back door blocked with spikes and IEDs

  - name: Site Traffic
    layout: chart
    data: hca_users
    context: Total users per week
    cols:
      - id: all
        label: Count of users

  - name: Mobile Usage
    layout: chart
    data: hca_mobile
    context: Percentage of users by device type used
    yLabel: Percentage
    yMax: 100
    cols:
      - id: mobile
        label: Mobile
        color: rgb(17,46,81)
      - id: desktop
        label: Desktop
        color: rgb(175,175,175)

  - name: New and Returning Users
    layout: chart
    data: hca_new
    context: Count of users
    cols:
      - id: new
        label: New
        color: rgb(17,46,81)
      - id: returning
        label: Returning
        color: rgb(175,175,175)
---

Only 10% of veterans apply for health care online...

...maybe because more than 70% of browsers are unable to access the application.
