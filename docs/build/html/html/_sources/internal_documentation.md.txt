# Internal documentation
This section describes, at a high, level, the internal documentation I created for different companies.\
\
Internal documentation is a vast field that includes:
- Troubleshooting.
- Procedures.
- Processes.
- Use of third-party tools.

I document all of them, depending on the company's needs.

***

## Internal documentation for 4Securitas
Here's how I worked on the internal documentation for 4Securitas:
- I created the structure of the documentation, dividing the topics into two: `Support Infrastructure` and `Support Troubleshooting`. The Infrastructure section has articles regarding knowledge or procedures. The Troubleshooting section has only articles regarding procedures on how to solve troubles internally.

```{figure} images/internal/4securitas_structure.png
:alt: The structure of the internal documentation for 4Securitas created by Federico Trotta.
:align: center

*The internal documentation structure I created for 4Securitas.*
```

- The articles are generally structured as step-by-step procedures, providing code or scripts as needed:

```{figure} images/internal/4securitas_article.png
:alt: An internal article for 4Securitas created by Federico Trotta.
:align: center

*An internal procedure I created for 4Securitas.*
```

***

## Internal documentation for DeAgostini
[DeAgostini](https://www.deagostini.com/) is the world leader in collectibles.\
\
As the only Technical Writer, I'm contributing to design and create their internal documentation to improve their employee explerience in their daily tasks.\
\
Here are the details of what I'm documenting for DeAgostini.

### The CMS documentation
DeAgostini developed internally a Content Management System (CMS) from scratch because there were no market solutions that could satisfy 100% their needs.\
\
I documented:
- The architecture.
- The dashboard management.
- What are the pages and how to manage the content.
- How to manage the products inside the pages.
- How to publish the content.

This documentation has been developed having in my the end user that, in their case, is mainly the Marketing Team. In other words, they developed the CMS from scratch so that the Marketing Team has custom software to advertise their products.

### Responsys documentation
They use [Responsys](https://www.oracle.com/it/cx/marketing/campaign-management/) to create marketing automation campaigns. It has [good documentation](https://docs.oracle.com/en/cloud/saas/marketing/responsys-user/Help/get_started.htm), but it's mainly feature-oriented and lacks use cases, so I documented how end users, that is the Marketing Team, can use it to:
- Create email campaigns.
- Create programs to automate the email campaigns.

I gave it the following structure:

**Getting started with Responsys**
- How to log in to Responsys.
- The process behind automated  email campaigns that is creating:
    - The email, per country.
    - The automation program.

**Managing campaigns**
- How to create a new email campaign.
- How to fill in the fields, in a standardized way.
- The auto-checks to control (users have to verify that some boxes are automatically checked).

**Managing automations**
- How to create a new automation program and what documentation to read from the Responsys website.
- A standardized way to show how the tens of active programs work.

### Jira documentation
DeAgostini uses Jira to manage internal tickets for internal requests.\

```{figure} images/internal/deagostini_jira.png
:alt: An image of the Jira dasbhboard documented by Federico Trotta for DeAgostini.
:align: center

*The internal Jira ticketing platform.*
```

I documented:
- How to log in to the platform.
- How to choose between an Incident Report, a Feature or Service Request, or a Customer Incident Report.
- How to fill in all the requested fields in a standardized way to improve the communication between internal departments. For example, we decided how and when users have to define if a task is urgent or not, for every kind of request.