---
title: Health Care Application
date_added: 2016-06-30 00:00:00 -0500
status: new
category: Apply
description: Making it easy to apply for VA health care online
tiles:
  - name: Daily Submissions
    layout: basic
    datapoint: 750
    context: on average

  - name: Fully automated
    layout: basic
    datapoint: 50%
    context: of submissions

  - name: Automated processing
    layout: compare
    datapoint: 50%
    before: 4%
    context: of applications can now be processed automatically

  - name: Mobile availability
    layout: icon
    icon: smartphone.svg
    text: Veterans can now complete their application entirely from a smartphone

  - name: User experience
    layout: image-compare
    before: no-acrobat-error.jpg
    after: healthcare.jpg

  - name: Veteran testimonial
    layout: quote
    text: The other website takes you around the corner, over the meadow, and...in a back door blocked with spikes and IEDs

  - name: Site Traffic
    layout: chart
    data: hca_sessions
    context: Total user sessions per day
    cols:
      - id: sessions
        label: Number of Sessions

  - name: Mobile Usage
    layout: chart
    data: hca_mobile
    context: Percentage of sessions by device type
    yLabel: Percentage
    yMax: 100
    cols:
      - id: mobile
        label: Mobile
        color: rgb(17,46,81)
      - id: desktop
        label: Desktop
        color: rgb(175,175,175)

  - name: New and Returning Veterans
    layout: chart
    data: hca_new
    context: Number of users
    cols:
      - id: new
        label: New
        color: rgb(17,46,81)
      - id: returning
        label: Returning
        color: rgb(175,175,175)
---