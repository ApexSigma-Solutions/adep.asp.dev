# Quickstart for writing on GitHub
Learn advanced formatting features by creating a README for your GitHub profile.

Who can use this feature?
Markdown can be used in the GitHub web interface.

In this article
Introduction
Markdown is an easy-to-read, easy-to-write language for formatting plain text. You can use Markdown syntax, along with some additional HTML tags, to format your writing on GitHub, in places like repository READMEs and comments on pull requests and issues. In this guide, you'll learn some advanced formatting features by creating or editing a README for your GitHub profile.

If you're new to Markdown, you might want to start with Basic writing and formatting syntax or the Communicate using Markdown GitHub Skills course.

If you already have a profile README, you can follow this guide by adding some features to your existing README, or by creating a gist with a Markdown file called something like about-me.md. For more information, see Creating gists.

Creating or editing your profile README
Your profile README lets you share information about yourself with the community on GitHub. The README is displayed at the top of your profile page.

If you don't already have a profile README, you can add one.

Create a repository with the same name as your GitHub username, initializing the repository with a README.md file. For more information, see Managing your profile README.
Edit the README.md file and delete the template text (beginning ### Hi there) that is automatically added when you create the file.
If you already have a profile README, you can edit it from your profile page.

In the upper-right corner of any page, click your profile picture, then click Your profile.

Click the  next to your profile README.

Screenshot of @octocat's profile README. A pencil icon is outlined in dark orange.
Adding an image to suit your visitors
You can include images in your communication on GitHub. Here, you'll add a responsive image, such as a banner, to the top of your profile README.

By using the HTML <picture> element with the prefers-color-scheme media feature, you can add an image that changes depending on whether a visitor is using light or dark mode. For more information, see Managing your theme settings.

Copy and paste the following markup into your README.md file.

HTML
<picture>
 <source media="(prefers-color-scheme: dark)" srcset="YOUR-DARKMODE-IMAGE">
 <source media="(prefers-color-scheme: light)" srcset="YOUR-LIGHTMODE-IMAGE">
 <img alt="YOUR-ALT-TEXT" src="YOUR-DEFAULT-IMAGE">
</picture>
Replace the placeholders in the markup with the URLs of your chosen images. Alternatively, to try the feature first, you can copy the URLs from our example below.

Replace YOUR-DARKMODE-IMAGE with the URL of an image to display for visitors using dark mode.
Replace YOUR-LIGHTMODE-IMAGE with the URL of an image to display for visitors using light mode.
Replace YOUR-DEFAULT-IMAGE with the URL of an image to display in case neither of the other images can be matched, for example if the visitor is using a browser that does not support the prefers-color-scheme feature.
To make the image accessible for visitors who are using a screen reader, replace YOUR-ALT-TEXT with a description of the image.

To check the image has rendered correctly, click the Preview tab.

For more information on using images in Markdown, see Basic writing and formatting syntax.

Example of a responsive image
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/25423296/163456776-7f95b81a-f1ed-45f7-b7ab-8fa810d529fa.png">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/25423296/163456779-a8556205-d0a5-45e2-ac17-42d089e3c3f8.png">
  <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="https://user-images.githubusercontent.com/25423296/163456779-a8556205-d0a5-45e2-ac17-42d089e3c3f8.png">
</picture>
How the image looks
Screenshot of the "Preview" tab of a GitHub comment, in light mode. An image of a smiling sun fills the box.

Adding a table
You can use Markdown tables to organize information. Here, you'll use a table to introduce yourself by ranking something, such as your most-used programming languages or frameworks, the things you're spending your time learning, or your favorite hobbies. When a table column contains numbers, it's useful to right-align the column by using the syntax --: below the header row.

Return to the Edit file tab.

To introduce yourself, two lines below the </picture> tag, add an ## About me header and a short paragraph about yourself, like the following.

## About me

Hi, I'm Mona. You might recognize me as GitHub's mascot.
Two lines below this paragraph, insert a table by copying and pasting the following markup.

Markdown
| Rank | THING-TO-RANK |
|-----:|---------------|
|     1|               |
|     2|               |
|     3|               |
In the column on the right, replace THING-TO-RANK with "Languages," "Hobbies," or anything else, and fill in the column with your list of things.

To check the table has rendered correctly, click the Preview tab.

For more information, see Organizing information with tables.

Example of a table
## About me

Hi, I'm Mona. You might recognize me as GitHub's mascot.

| Rank | Languages |
|-----:|-----------|
|     1| JavaScript|
|     2| Python    |
|     3| SQL       |
How the table looks
Screenshot of the "Preview" tab of a GitHub comment. Under the "About me" heading is a rendered table with a ranked list of languages.

Adding a collapsed section
To keep your content tidy, you can use the <details> tag to create an expandable collapsed section.

To create a collapsed section for the table you created, wrap your table in <details> tags like in the following example.

HTML
<details>
<summary>My top THINGS-TO-RANK</summary>

YOUR TABLE

</details>
Between the <summary> tags, replace THINGS-TO-RANK with whatever you ranked in your table.

Optionally, to make the section display as open by default, add the open attribute to the <details> tag.

<details open>
To check the collapsed section has rendered correctly, click the Preview tab.

Example of a collapsed section
<details>
<summary>My top languages</summary>

| Rank | Languages |
|-----:|-----------|
|     1| JavaScript|
|     2| Python    |
|     3| SQL       |

</details>
How the collapsed section looks
Screenshot of the "Preview" tab of a comment. To the left of the words "Top languages" is an arrow indicating that the section can be expanded.

Adding a quote
Markdown has many other options for formatting your content. Here, you'll add a horizontal rule to divide your page and a blockquote to format your favorite quote.

At the bottom of your file, two lines below the </details> tag, add a horizontal rule by typing three or more dashes.

---
Below the --- line, add a quote by typing markup like the following.

> QUOTE
Replace QUOTE with a quote of your choice. Alternatively, copy the quote from our example below.

To check everything has rendered correctly, click the Preview tab.

Example of a quote
---
> If we pull together and commit ourselves, then we can push through anything.

— Mona the Octocat
How the quote looks
Screenshot of the "Preview" tab of a GitHub comment. A quote is indented below a thick horizontal line.

Adding a comment
You can use HTML comment syntax to add a comment that will be hidden in the output. Here, you'll add a comment to remind yourself to update your README later.

Two lines below the ## About me header, insert a comment by using the following markup.

<!-- COMMENT -->
Replace COMMENT with a "to-do" item you remind yourself to do something later (for example, to add more items to the table).

To check your comment is hidden in the output, click the Preview tab.

Example of a comment
## About me

<!-- TO DO: add more details about me later -->
Saving your work
When you're happy with your changes, save your profile README by clicking Commit changes.

Committing directly to the main branch will make your changes visible to any visitor on your profile. If you want to save your work but aren't ready to make it visible on your profile, you can select Create a new branch for this commit and start a pull request.