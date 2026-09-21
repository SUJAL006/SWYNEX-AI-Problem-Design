# Route dining-hall comments. Don’t build another campus chatbot.
Most “AI on campus” pitches are too wide: a tutor for every course, a copilot for every office. This one is small on purpose.
**The job:** take short comments from one dining hall’s QR form and propose a single label — food quality, wait time, cleanliness, or other — so the right person sees the ticket first. A coordinator still decides what to do. The model does not reply to students.
## Who it is for
The primary user is the dining operations coordinator for one residential hall. Kitchen, service, and facilities leads are downstream. Success is a weekday morning inbox that clears in under 15 minutes, with cleanliness issues never sitting unnoticed.
## Data
About 320 English comments from one hall, one semester, 1–3 sentences each. Two staff raters label independently; the coordinator breaks ties. Names, emails, and IDs are stripped before anything is trained. No social media scrape. No student information system.
Labels are exclusive. Mixed or off-topic comments become **other**. Cleanliness is the safety-adjacent class (spills, dirty stations, pests).
## Constraints
- One label only. No generated replies, refunds, or public posts.
- If the top-class probability is below 0.70, leave it unlabeled for the coordinator.
- Predicted cleanliness always jumps the queue.
- English only for v1.
- Hourly batch scoring is enough. Comments stay in campus cloud under a data-processing agreement.
- Staff UI must work with keyboard and screen readers; labels are words, not color alone.
- Raw text older than two semesters is deleted.
## How we would know it works
Frozen holdout of 80 comments. Ship only if we beat a keyword baseline.
- Macro-F1 at least 0.78 (and +0.08 over keywords).
- Cleanliness recall at least 0.90 — every miss is read.
- Precision at least 0.80 on wait time and food quality.
- Abstain rate between 10% and 25%.
- Shadow mode for 10 weekdays before any auto-routing. Median handling time should fall from ~45 seconds per comment to under 15.
If rater agreement (Cohen’s kappa) is below 0.70, we fix the label guide rather than tuning the model. If cleanliness recall misses the bar, we do not ship routing.
## What this is not
Not a sentiment dashboard. Not automated student email. Not training on Yelp. Not a substitute for health-department reporting.
The useful version is boring: four labels, one hall, one form, a holdout set you can read in an afternoon, and a human who still owns the queue.
---
*Illustrative examples only; no student records.*
