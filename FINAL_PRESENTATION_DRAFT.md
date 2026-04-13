# Final Presentation Draft

## Presentation Goal

This draft is designed for a 10-minute presentation with about 2 minutes left for Q&A and setup.

Recommended structure:

1. 8 slides total
2. About 60-75 seconds per main slide
3. 2 minutes for demo transitions and Q&A

---

## Title Slide

**LangLocalJobs: A Full-Stack Job Board for Language and Localization Professionals**

Subtitle:

- APPD5016 / Full Stack Skills Exploration and Development
- Your name
- Presentation date

Speaker notes:

Hello everyone. My area of study this term was full-stack web development, with a focus on building an automated job board platform for language and localization professionals. My project is called LangLocalJobs, and today I will briefly explain what I studied, the materials I used, how the project developed over the term, and then I will demonstrate the final product.

---

## Slide 1: Area of Study

**Area of study**

- Full-stack web development
- Flask backend + React frontend
- Job data ingestion through scraping and public APIs
- User and admin workflows

Speaker notes:

My area of study was full-stack web development. I specifically wanted to learn how a backend API, a frontend interface, a database, and external data sources can work together in one project. To explore that, I built LangLocalJobs, which is a job board application that collects job listings, stores them in a database, and lets users browse, save, and track jobs.

---

## Slide 2: Why I Chose This Topic

**Why this topic**

- Strong employability value in full-stack development
- Personal interest in building a practical web platform
- Good way to combine backend, frontend, databases, and APIs in one project
- Relevant to real-world product development

**Prior knowledge**

- I already had some programming experience, but limited experience building a complete full-stack application from start to finish
- I especially wanted more hands-on practice with Flask architecture, React integration, authentication, and database design

Speaker notes:

I chose this topic for both employability and personal interest. Full-stack development is a very practical skill because it combines multiple areas that employers often look for, including backend logic, frontend development, databases, authentication, and debugging. Before this class, I had some programming knowledge, but I had not built a complete application like this from start to finish with both a backend and frontend working together.

If needed, personalize this sentence:

"Before this class, I was most comfortable with [Python / frontend basics / general programming], but I had less experience with [Flask APIs / React / database migrations / web scraping]."

---

## Slide 3: Study Materials I Used

**Main study materials**

- Flask documentation
- SQLAlchemy documentation
- BeautifulSoup documentation
- MDN Web Docs
- W3Schools
- GitHub and my Kanban board
- Class guidance and project milestones

**My opinion of the materials**

- Official documentation was the most reliable and detailed
- MDN was very useful for frontend concepts and browser behavior
- W3Schools was helpful for quick refreshers, but not deep enough by itself
- GitHub Kanban helped me stay organized week by week

**Would I recommend them?**

- Yes, especially the official docs and MDN
- I would recommend W3Schools only as a quick secondary reference

Speaker notes:

The resources I used most were the official documentation for Flask, SQLAlchemy, and BeautifulSoup, along with MDN for frontend topics. I also used W3Schools for quick reminders when I needed a simple example fast. My opinion is that official documentation gave me the best accuracy, while MDN was great for frontend details. I would recommend official docs first, MDN second, and W3Schools only as a quick support resource rather than a main learning source.

Visuals to show on this slide:

- Screenshot of your bookmarks, notes, or the documentation home pages
- Optional screenshot of your GitHub repo or Kanban board

---

## Slide 4: Project Overview and Tech Stack

**What I built**

- A job board web application called LangLocalJobs
- Users can register, log in, browse jobs, save jobs, and mark jobs as applied
- Admins can view users, manage job listings, and review applied jobs

**Tech stack**

- Frontend: React, React Router, TanStack Query, Tailwind CSS
- Backend: Python, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-CORS
- Database: SQLite in development, PostgreSQL planned for production
- Authentication: JWT
- Data ingestion: Requests + BeautifulSoup + public job APIs

Speaker notes:

The final product is a full-stack application with a React frontend and a Flask backend. The system includes authentication, database models, protected routes, job browsing, saved jobs, applied jobs, and an admin dashboard. For data ingestion, I used public APIs and scraping-related tooling to collect and normalize job listings before storing them in the database.

Important honesty point:

My original idea focused more narrowly on language and localization jobs. In the final implementation, I built the ingestion pipeline as a proof of concept using accessible public job sources, which means the architecture is working even though the niche data sources could still be expanded further.

---

## Slide 5: Kanban Board and Weekly Breakdown

**Kanban final state**

- Most core tasks moved to Done
- A few stretch goals remained as future improvements

Show this live:

- Screenshot of your final Kanban board
- Point out `Done`, `In Progress`, and any remaining backlog items

**Very brief weekly breakdown**

- Week 1: Research, project scope, repo setup, environment setup, initial documentation
- Week 2: Core backend structure, database models, migrations, and first scraping work
- Week 3: Multi-source job ingestion, authentication, frontend integration, save and apply features
- Week 4: Admin dashboard, search and filters, date filtering, more data, database improvements
- Week 5: Polishing, documentation, job details improvements, presentation preparation

Speaker notes:

My Kanban board helped me break the project into manageable weekly tasks. In week 1, I focused on planning and setup. In week 2, I built the backend foundation. In week 3, I added multi-source ingestion and authentication, then connected the frontend. In week 4, I expanded the admin features and improved filtering. In week 5, I focused on cleanup, documentation, and preparing the final presentation.

Optional future-backlog items to mention if they appear on your board:

- More language-specific job sources
- Recruiter self-service posting flow
- Better automated test coverage
- Deployment and hosting

---

## Slide 6: Final Product Demonstration

**Demo plan**

1. Show the home page
2. Register or log in
3. Open the jobs page
4. Search or filter by title, company, location, or date
5. Open a job details page
6. Save a job
7. Mark a job as applied
8. Open the user dashboard to show saved and applied jobs
9. If time permits, log in as admin and show admin dashboard tabs

**Note**

- The project does not need to be hosted
- I will run it locally for the demonstration

Speaker notes:

For the demo, I'll show the user journey first. I'll log in, browse jobs, use the filters, open a job details page, save a job, and mark one as applied. Then I'll show the dashboard where those actions are tracked. If time allows, I'll also show the admin dashboard, where an admin can view users, browse job records, and see all recorded applications.

Live demo tips:

- Start both servers before class if possible
- Keep one test user ready
- Keep one admin user ready
- Have a backup as screenshots in case the demo is slow

---

## Slide 7: Challenges and Issues

**Main challenges**

- Connecting frontend and backend cleanly
- Managing authentication with JWT across protected routes
- Designing and updating the database schema during development
- Normalizing job data from multiple external sources
- Avoiding duplicate job entries
- Balancing project scope with available time

**How I handled them**

- Used a modular Flask structure with separate routes and services
- Used migrations to evolve the schema instead of rebuilding everything manually
- Added duplicate detection and update logic in the scraping service
- Reduced scope where necessary and focused on a working end-to-end product

Speaker notes:

The biggest technical challenge was getting all the moving parts to work together consistently. Authentication was one challenge, because I needed protected routes and role-based access. Another challenge was data ingestion, because different APIs and sources return data in different shapes, so I had to normalize and store them consistently. Scope was also a challenge. My initial vision was bigger than what could reasonably be polished in one term, so I focused on delivering a working proof of concept with core features completed.

Useful honest point:

One thing I would improve next is automated testing. The project has structure for tests, but test coverage is still limited, so that is one of the clearest areas for future growth.

---

## Slide 8: Final Thoughts

**Final thoughts on the technology**

- Flask was approachable and flexible for building the API
- React made it easier to separate pages and user interactions
- SQLAlchemy and migrations were useful, but required careful planning
- Working across the full stack gave me a much better understanding of how web applications are built end to end

**Would I use this technology again?**

- Yes
- I would continue with Flask for small to medium projects
- I would keep React for interactive frontends
- For future work, I would strengthen testing, deployment, and source-specific data pipelines

Speaker notes:

Overall, I had a positive experience with this technology stack. Flask felt lightweight and understandable, which made it a good choice for learning backend architecture. React helped me organize the frontend into reusable pages and components. This project gave me a better understanding of how real applications move data from an external source into a database and then into a user interface. I would definitely use this stack again, especially now that I understand its strengths and the areas where I still want to improve.

Closing sentence:

In summary, this project helped me grow from studying isolated tools to actually building an end-to-end product, and that was the most valuable part of the experience.

---

## Q&A Slide

**Questions?**

Short closing line:

Thank you for listening. I'd be happy to answer any questions.

---

## Short 10-Minute Speaking Version

If you want a tighter version, this is a simple talk flow:

1. Introduce the topic and project in 30 seconds
2. Explain why you chose full-stack development in 45 seconds
3. Cover your learning materials and opinions in 60 seconds
4. Explain the project and stack in 75 seconds
5. Show Kanban and weekly progress in 75 seconds
6. Demo the app in about 3 minutes
7. Explain challenges and final thoughts in 90 seconds
8. Leave the last minute or two for questions

---

## Demo Checklist for Class Day

- Open your slide deck
- Open your final Kanban screenshot
- Start backend server
- Start frontend server
- Keep test login ready
- Keep admin login ready
- Keep backup screenshots ready in case the live demo fails
- Test projector connection in advance if using your own laptop

---

## Possible Questions and Good Answers

**Why did you choose Flask instead of Django?**

I chose Flask because it is lighter weight and helped me understand the application structure more directly. For this course, it was a good fit for learning how the backend pieces connect.

**What would you improve next?**

I would add stronger automated testing, improve deployment, and expand the data sources so the job listings are even more targeted to language and localization roles.

**What was the hardest part?**

The hardest part was connecting multiple moving parts at once: authentication, database design, frontend integration, and external job data.

**What are you most proud of?**

I'm most proud that the project works end to end. A user can log in, browse jobs, save jobs, mark them as applied, and an admin can manage platform data.

---

## Personalization Notes

Before presenting, replace or adjust these items:

- Add your name and presentation date
- Add a screenshot of your real Kanban board
- Adjust the prior-knowledge sentence so it matches your real experience
- If you used extra resources like YouTube, Stack Overflow, or class notes, add them
- If you do not want to show the admin dashboard live, remove that part from the demo plan
