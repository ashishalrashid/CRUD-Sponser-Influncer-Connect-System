# Influencer Engagement and Sponsorship Coordination Platform

## Overview
A platform designed to connect Sponsors and Influencers, enabling Sponsors to advertise their products/services and Influencers to gain monetary benefits.

This project successfully implements all the required features and functionality described below.

---

## Frameworks Used

The platform is built using the following frameworks:

- **Flask**: For application logic and backend routing.
- **Jinja2 Templates + Bootstrap**: For dynamic HTML generation and responsive styling.
- **SQLite**: For efficient and lightweight data storage.

**Note**: All functionalities can be demonstrated locally.

---

## Roles

### 1. **Admin** (root access)
- Monitor all users and campaigns, and view application statistics.
- Ability to flag inappropriate campaigns or users.
- Ban or dismiss flagged users or sponsors.

### 2. **Sponsors**
- Create and manage campaigns.
- Search for influencers and send ad requests for campaigns.
- Track the progress of campaigns and manage ad requests.

Attributes for Sponsors:
- Company/Individual Name
- Industry
- Budget

### 3. **Influencers**
- Receive, accept, or reject ad requests.
- Negotiate terms and resend modified ad requests.
- Search for public campaigns and accept relevant requests.
- Maintain and update a public profile.
- Report misuse by sponsors if necessary.

Attributes for Influencers:
- Name
- Category
- Niche
- Reach (calculated by number of followers/activity, etc.)

---

## Terminologies

### **Ad Request**
A contract between a campaign and an influencer, specifying advertisement requirements, payment amount, and status.

Attributes:
- `campaign_id`: Foreign key to Campaign table
- `influencer_id`: Foreign key to Influencer table
- `messages`
- `requirements`
- `payment_amount`
- `status`: (Pending, Accepted, Rejected)

### **Campaign**
A container for ad requests associated with a specific advertising goal (e.g., Samsung S23 launch). It can have multiple attributes:

Attributes:
- `name`
- `description`
- `start_date`
- `end_date`
- `budget`
- `visibility`: Public or Private
- `goals`

---

## Core Functionalities Implemented

### 1. **User Authentication**
- Login/Register forms for Admin, Sponsors, and Influencers with fields like username and password.
- Differentiation of user roles via a suitable model.

### 2. **Admin Dashboard**
- Displays relevant statistics:
  - Active users
  - Public and private campaigns
  - Ad request statuses
  - Flagged users (sponsors/influencers)
- Additional statistics as deemed necessary.
- Ability to ban or dismiss flagged users or sponsors.

### 3. **Campaign Management** (for Sponsors)
- Create new campaigns and categorize by niche.
- Update campaign attributes such as start date, end date, or budget.
- Delete existing campaigns.

### 4. **Ad Request Management** (for Sponsors)
- Create ad requests aligned with campaign goals.
- Edit ad request attributes like influencer ID, requirements, payment amount, or status.
- Delete ad requests.

### 5. **Search Functionality**
- **Sponsors**: Search for relevant influencers based on niche, reach, followers, etc.
- **Influencers**: Search for public campaigns based on niche and relevance.

### 6. **Ad Request Actions** (for Influencers)
- View all ad requests from various campaigns.
- Accept or reject specific ad requests.
- Negotiate payment amounts for ad requests.

### 7. **Flagging System**
- Influencers and Sponsors can report misuse of the platform.
- Admins can review flagged users and take appropriate action (ban or dismiss flags).

---
## E-R diagram
![ER Diagram](github_assets/er%20diagram.jpg)



