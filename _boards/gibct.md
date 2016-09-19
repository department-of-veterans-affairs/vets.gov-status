---
title: GI Bill Comparison Tool
date_added: 2015-11-01 00:00:00 -0500
vetsdotgov_url: https://www.vets.gov/gi-bill-comparison-tool/
status: normal
category: Discover
description: Now includes performance metrics on schools--and caution flags
tiles:

  - name: User Experience
    layout: image-compare
    before: old-healthcare.jpg
    after: healthcare.jpg

  - name: Mobile availability
    layout: compare
    datapoint: 100%
    before: 46%
    context: of content available on mobile devices

  - name: Daily Submissions
    layout: basic
    datapoint: 750
    context: on average

  - name: Veteran testimonial
    layout: quote
    text: The other website takes you around the corner, over the meadow, and...in a back door blocked with spikes and IEDs

  - name: Site Traffic
    layout: chart
    data: gibct_users
    context: Total users per week
    cols:
      - id: all
        label: Count of users

  - name: Mobile Usage
    layout: chart
    data: gibct_mobile
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
    data: gibct_new
    context: Count of users
    cols:
      - id: new
        label: New
        color: rgb(17,46,81)
      - id: returning
        label: Returning
        color: rgb(175,175,175)
---
