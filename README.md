# Mammas-Cakes

![Website mock-up](media/docs/mockup.png)

Mammas Cakes is an e-commerce website project created for a imaginary bake shop in UK. The main goal of this project was to create the most user-friendly website possible, where you can shop for cakes in an easy and intuitive way. The user can view collection of products, place an order  as a collection or delivery . Users need to register their login credentials and be authenticated before placing an order. Registered users also have the option to view their order history  

Project was created using Python, Django, HTML5, CSS3, and JavaScript. The data was stored in a PostgreSQL database manipulation and deployed using Heroku. Mammas Cakes is my third milestone project for Code Institute's Level 5 Diploma in Web Application Development. Languages used: HTML, CSS, Javascript, Python and Django

[View the live site](
https://git.heroku.com/mammas-cakes.git/)

# Table content
* [UX & 5 Placen of Webiste Design](#ux-and-five-planes-of-website-design)
    * [Strategy](#strategy)
    * [Structure](#structure)
    * [Skeleton](#skeleton)
    * [Surface](#surface)
* [Features](#features)
    * [Home Page](#home-page)
    * [Product Page](#products-page)
    * [Profile Page](#profile-page)
    * [Contact Form](#contact-form)
    * [Authentication](#authentication)
* [Technologies](#technologies-used)
* [Testing](#testing)
  * [Validation](#validation)
    * [HTML Validation](#html-validation)
    * [CSS Validation](#css-validation)
    * [JavaScript Linting](#javascript-linting)
    * [Python Linting](#python-linting)
    * [Lighthouse Testing](#lighthouse-testing)
    * [Responsiveness](#responsiveness)
* [Manual Testing](#manual-testing)
* [User Stories Testing](#user-stories-testing)
* [Bugs, Issues and Solutions](#bugs-issues-and-solutions)
* [Future Enhancements](#Future Enhancements)
* [Deployment](#deployment)
* [Credits](#credits)

  # UX and Five Planes of Website Design

## Strategy

### User stories

1. As a first time user I want to:
* Immediately understand the main purpose and use of the site
* Be able easily navigate through the site
* Select navigation links of products offered
* View collection of each product type
* Contact the company regarding any queries
* Be able use the page on any devices and screen sizes
* View Social media links and pages from the site
* Register a customer account

2. As a registered user I want to:
* Place an order for my desired product
* Complete my order details
* Complete a collection or delivery order
* Receivie confirmation of my order on screen and as an email.
* View my Order History
* Be able to change my password, if I have forgotten my login details

3. As an admin I want to:
* Be able to add, edit and delete cakes
* Be able to change the status of orders
* be able to edit user profile details
* Be able to view customer cake orders
* Be able to reset customer passwords
* Have easy access to admin controls

## Structure

 ### Database Schema
The database was designed using DpDiagram.io. There are 5 tables within this relational database: User, Cake, Customer, Order and OrderItem.
<details><summary>ERD</summary>
<img src="static/images/erdcakes.png">
</details>


## Skeleton
   ### Wireframes

<details><summary>Home Page</summary>
<img src="static/images/mammashomewf.png">
</details>
<details><summary>Templates</summary>
<img src="static/images/mammastemplateswf.png">
</details>
<details><summary>Account Creation</summary>
<img src="static/images/mammasregisterwf.png">
</details>
<details><summary>Login</summary>
<img src="static/images/mammasloginwf.png">
</details>
<details><summary>Order Confirm</summary>
<img src="static/images/orderconfirmwf.png">
</details>

## Surface

### **Colour** 
The Colour palette is a mixture of 3 colours. Dark blue for the header, white colour for the main body and light blue for the footer.The buttons consists of blue colours too.
 

### **Typography** 

Fonts were imported from [Google Fonts](https://fonts.google.com/). 

I selected  "Arial"  as the primary font for the main body and Sans-Serif as the Secondary font . I found the Aerial font is a simple, user-friendly, outstanding and clean typeface that contributes the design. 
I selected light blue, white as the main body colors and purple for the footer.

# Features

## Home Page

## User Functionality

<details><summary>Home Page</summary>
Site is opened on this page
<img src="static/images/mammashome.png">
</details>
<details><summary>Product</summary>

Customers can view selection of cakes on offer, ranging from Birthday, Wedding, Treats and Vegan Cakes.
<img src="static/images/mammasproducts.png">
</details>
<details><summary>Login</summary>
<img src="static/images/cakeslogin.png">
</details> Customer are required to login before placing an order
<details><summary>Create Order</summary>
<img src="static/image/createorder.png">
</details>Customers need to complete all fields before submitting their order
<details><summary>Order Confirm</summary>
<img src="static/images/orderconfirm.png">
</details>Once order has been submitted, customers receive a confirm alert on screen
<details><summary>Email Confirmation</summary>
<img src="static/images/mailconfirmation.png">
</details>Once order has been submitted, customers receive an email confirmation
<details><summary>Order History</summary>
<img src="static/images/cakesorderhistory.png">
</details> Customer can view their orders whilst logged in to their profile
<details><summary>Registration</summary>
<img src="static/images/register.png">
</details> It's mandatory for customers to register, if they already heavent to place an orde
<details><summary>Password Reset</summary>
<img src="static/images/passwordreset.png">
</details> Customers can request a password reset should they forget their login details. Entering an email address registered on our system will enable them to receive a password reset link to reset their password.
<details><summary>Contact Us</summary>
<img src="static/images/contactus.png">
</details> Customer can contact the firm about any query via the form
<details><summary>Contact Mail Confirmation</summary>
<img src="static/images/contactrequestmail.png">
</details> Confirmation the business has received a contact request query

 ## Site Admin 
Site Administrators only have priveleges to modify the site, add products, manage customer orders using super user login credentials. Please see below the 
<details><summary>Admin Site Login</summary>
<img src="static/images/adminlogin.png">
</details> Administrators can login via the site home page using their super user credentials.
<details><summary>Site Administration</summary>
<img src="static/images/siteadmin.png">
</details> Administrators can manage this section to add and remove cake products, add, change and remove customer information an and manage customer orders.
<details><summary>Cake Admin</summary>
<img src="static/images/addcake.png">
</details> Administrators can add and remove cake products via the cakes link
<details><summary>View Orders</summary>
<img src="static/images/vieworders.png">
</details> Administrators canv view orders arrived through the site.
<details><summary>Change Order</summary>
<img src="static/images/orderchange.png">
 Admins can change the order. Very useful and repetitive when changing status of an order from pending to available to collect or delivered.
 </details>

## Technologies Used

-   ### Frameworks, Libraries & Programs Used

    * [Google Fonts](https://fonts.google.com/) were used to import the 'Bebas Neue' and 'Noto Serif' font into the style.css file which is used on all pages throughout the project. 
    * [Bootstrap v5.3.2]() was used on all pages throughout the website to add icons for aesthetic and UX purposes.
    * [Visual Studio Code](https://code.visualstudio.com)/) was the IDE used to build the project. 
    * [GitHub](https://github.com/) is used to store the projects code after being pushed from Git.
    * [Balsamiq](https://balsamiq.com/) was used to create the wireframes to support in the design process.
    * [Pip](https://pypi.org/project/pip/) - tool for installing python packages.
    * [DPDiagram](https://dpdiagram.io) was used to design the EDR model when planning the database.
    * The site was deployed using [Heroku](https://www.heroku.com) and the database used alongside this was PostgreSQL fro Code Institute.
    * [Favicon.io](https://favicon.io/) was used to design the favicon for the site.
    * [Cloudinary] (https://cloudinary.com/) used to transform digital images via the Heroku platform.
    * [Chrome Developer Tools](https://developer.chrome.com/docs/devtools) was used throughout, to troubleshoot, solve bugs, test site features and responsiveness
    * [amiresponsive](https://ui.dev/amiresponsive) was used to create the responsive screen imagery for the site.
I decided use the built in Django instead of Django all-auth for its simplicity to manage authentication of customers.

# Testing 

# Validation 
## HTML Validation
Variious html pages shows a mixture of pass and fails. W3 Validator sees % extends cake/base.html' % and does not recognize. Validator cannot parse Django Syntax. By creating a static template to pass validaton, would miss template inheritance and dynamic content. Using page source, rendered html and pasting code into html validator returns 0 error and warnings.All pages show no errors when entered using page source.

| Template                    | Result                                                                                                                                                                                                                                                                                                                | Pass/Fail | Reason for Fail                                        |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ------------------------------------------------------ |
| Base.html                   | Non space errors found, element missing head, strey doc type, stray startup                                                                                                                                                                                                                                           | Fail      | because W3 validator not understanding django template |
| Home                        | Non space value, bad attributes src on elements                                                                                                                                                                                                                                                                       | Fail      | because W3 validator not understanding django template |
| Products                    | Fail                                                                                                                                                                                                                                                                                                                  | Fail      | because W3 validator not understanding django template |
| Birthday                    | Non space errors found, element missing head, bad value for attribute on element                                                                                                                                                                                                                                      | Fail      | because W3 validator not understanding django template |
| Wedding                     | Non space errors found, element missing head, bad value for attribute on element                                                                                                                                                                                                                                      | Fail      | because W3 validator not understanding django template |
| Treats                      | Non space errors found, element missing head, bad value for attribute on element                                                                                                                                                                                                                                      | Fail      | because W3 validator not understanding django template |
| Vegan                       | Non space errors found, element missing head, bad value for attribute on element                                                                                                                                                                                                                                      | Fail      | because W3 validator not understanding django template |
| Signup                      | No Warnings                                                                                                                                                                                                                                                                                                           | Pass      |                                                        |
| Register                    | No Warnings                                                                                                                                                                                                                                                                                                           | Pass      |                                                        |
| Login                       | No Warnings                                                                                                                                                                                                                                                                                                           | Pass      |                                                        |
| Order Confirmation Email    | No Warnings                                                                                                                                                                                                                                                                                                           | Pass      |                                                        |
| Order History               | No Warnings                                                                                                                                                                                                                                                                                                           | Pass      |                                                        |
| Order Detail                | No Warnings                                                                                                                                                                                                                                                                                                           | Pass      |                                                        |
| Order Confirmation          | No Warnings                                                                                                                                                                                                                                                                                                           | Pass      |                                                        |
| Password reset request      | Non space errors found, element missing head, bad value for attribute on element                                                                                                                                                                                                                                      | Fail      | because W3 validator not understanding django template |
| Password reset confirmation | Non space errors found, element missing head, bad value for attribute on element                                                                                                                                                                                                                                      | Fail      | because W3 validator not understanding django template |
|                             | W3 Validator sees % extends cake/base.html' % and does not recognize. Validator cannot parse Django Syntax. By creating a static template to pass validaton, would miss template inheritance and dynamic content. Using page source, rendered html and pasting code into html validator returns 0 error and warnings. |           |                                                        |

## CSS Validation
I run the CSS code through [W3C CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input) and showed No errors.
<img src="static/images/cssvalidator.png">

## JavaScript Linting

<details><summary>JavaScript Linting</summary>
<img src="static/images/cakesjsint.png">
</details> I ran the JavaScript code through [JSHint](https://jshint.com/), I only had one js file to run the code order-system.js. Two warnings  and one undefined bootstrap variables, which have been resolved.

## Python Linter

I ran the code through [CI Python Liner](https://pep8ci.herokuapp.com/), which shows a multiple errors mostly regarding blank lines, missing whitespaces and too long lines, which all were fixed.

| App          | File                   | Result                                       | Fixed |
| ------------ | ---------------------- | -------------------------------------------- | ----- |
| Cakes        | views                  | lines too long (81, 246, 250, 254, 269, 274) | Yes   |
| Cakes        | models                 | line 94 too long                             | Yes   |
| Cakes        | forms                  | line 109, 132 too long                       | yes   |
| Cakes        | admin                  | All ok                                       | yes   |
| Cakes        | urls                   | no new line at end                           | yes   |
| Cakes        | settings               | lines 93, 96, 92 102 too long                | Yes   |
| Migration    | 0001_initial.py        | spacing and long line                        | Yes   |
| Migration    | 00021_order_collection | All ok                                       | yes   |
| Migration    | 0003_order_update      | All ok                                       | yes   |
| Migration    | 0004_alter             | All ok                                       | Yes   |
| Mammas-Cakes | urls.py                | All ok                                       | Yes   |
| Mammas-Cakes | manage.py              | All ok                                       | Yes   |
| Mammas-Cakes | env.py                 | All ok                                       | Yes   |

## Lighthouse Testing
The site was run through Google Chrome Dev Tools Lighthouse. Results were excellent, close to 100% for majority. See below

#### For full results see dropdown below

### Desktop

<details><summary>Home Page</summary>
<img src="static/images/cakeslighthousehome.png">
</details>
<details><summary>Birthday Cakes</summary>
<img src="static/images/cakesbirthdaylighthouse.png">
</details>
<details><summary>Wedding Cakes</summary>
<img src="static/images/cakeslighthousewedding.png">
</details>
<details><summary>Treats</summary>
<img src="static/images/cakeslighthousetreats.png">
</details>
<details><summary>Vegan Cakes</summary>
<img src="static/images/cakesveganlighthouse.png">
</details>
<details><summary>Order History</summary>
<img src="static/images/cakesorderhistorylighthouse.png">
</details>
<details><summary>Registration</summary>
<img src="static/images/cakesregisterlighthouse.png">
</details>
<details><summary>Login</summary>
<img src="static/images/cakesloginlighthouse.png">
</details>
<details><summary>Password Reset</summary>
<img src="static/images/cakespasswordlighthouse.png">
</details>
<details><summary>Contact Form</summary>
<img src="static/images/cakescontactlighthouse.png">
</details>

## Responsiveness

I checked my site on Chrome devtools dimensions and all devices listed had a user friendly view and all pages and links were clearly visible and navigational. The site was tested on Iphone X, and Ipad Pro on Chrome and Safari we browsers and demonstrated quality display and functionality. Order could be placed sucessfully and links were operational.



# Manual Testing
I conducted comprehensive manual testing on my page, ensuring all functions, links and button functioned correctly. I verified the layout and design, checked the responsiveness and reviewed the content for accuracy. All successfully passed the thorough testing, ensuring its user-friendly navigational, form submission functionality and reliability.

<details><summary>User Link Navigation</summary>

| Test Page                   | Goal                                                                        | Result |
| --------------------------- | --------------------------------------------------------------------------- | ------ |
| Home Page                   | Cake Collection categories Visible with images and option to view and order | Pass   |
| Cake type Navigation links  | Visible on all page                                                         | Pass   |
| Birthday Cakes link         | All birthday cakes visible with price, description and order button         | Pass   |
| Wedding Cakes link          | All Wedding cakes visible with price, description and order button          | Pass   |
| Treat Cake Link             | All treat cakes visible with price, description and order button            | Pass   |
| Vegan Cake Link             | All  Vegan cakes visible with price, description and order button           | Pass   |
| Register Link               | Opens up registration form                                                  | Pass   |
| Forgotten you password link | Opens window to enter email address                                         | Pass   |
| Order History               | Available whilst logged in                                                  | Pass   |
| Footer                      | Visible on all page                                                         | Pass   |
| Quick links                 | All navigation links functional                                             | Pass   |
| Social networking Links     | All links functional and open up an external page                           | Pass   |
| Contact form                | Fully functional and received by email to mammas.cakes16@gmail.com          | Pass   |

</details>

<details><summary>User Functions</summary>

| Function                                                  | Goal                                                          | Result |
| --------------------------------------------------------- | ------------------------------------------------------------- | ------ |
| Login Now Button                                          | Opens with login window                                       | Pass   |
| Order Now Button                                          | Visible and clickable when user is logged in                  | Pass   |
| Order Form not available without login                    | User needs to be registered and logged in                     | Pass   |
| Order form required to complete all fields before sending | Any fields empty prompts with an alert message                | Pass   |
| Delivery or Collection                                    | Option to switch between both                                 | pass   |
| Delivery Address prompt ?                                 | Prompted to enter address detail on delivery only             | Pass   |
| Order Confirmation message                                | Visible on screen and received by email with required details | pass   |

</details>

<details><summary>Admin Functions</summary> Test
   
| Test Function                                   | Goal                                                                  | Result |
| ----------------------------------------------- | --------------------------------------------------------------------- | ------ |
| Login as super user                             | Opened up admin panel                                                 | Pass   |
| Add Cake products                               | Opens up form to add cake with image, price, description and category | Pass   |
| Adjust registered customer email address        | Click users, clicking on their username and make change               | Pass   |
| Change registered customer contact phone number | Click customer and adjust phone number                                | Pass   |
| View customer order                             | Order queue listed                                                    | Pass   |
| Option to change order status                   | Clicking on order and change status                                   | Pass   |
| Change Customer password                        | Click users, open their profile, complete form to create new password | Pass   |
| Remove customer                                 | select customer and  delete                                           | Pass   |
| Remove Cake                                     | select Cakes, select cake and action by delete                        | Pass   |

</details>


# Bugs, Issues and Solutions

| Problem/Error                                                                                          | Solution                                                                                                                   | Fixed |
| ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- | ----- |
|                                                                                                        |                                                                                                                            |       |
| No function when clicking order now button                                                             | validation in javascript file needed adjusting                                                                             | Yes   |
| Order form submitted without all input fields being completed                                          | Added helper function to views.py and adjusted validation method in js file                                                | Yes   |
| No emails generated when order is submitted. Recepient not receiving email confirmation                | Adjusted order confirmation template                                                                                       | Yes   |
| Programming Error when running server, resulting in server 500 console error                           | Changed database configuration in settings.py. Database corrupted and had to create new Postreqsql                         | Yes   |
| Failed to submit for pop up error when attempting to create order, uncaught type error                 | Fixed method in js file                                                                                                    | Yes   |
| error 400 in terminal , "your accessing dev server over https" Http 400 error on dev tools             | Adjusted date parsing in views.py                                                                                          | yes   |
| Orders generated as collection order when delivery is requested.                                       | Updated delivery address fields in models.py and adjsuted validation logic in js file                                      | yes   |
| After creating a registration template, receiving error "django core exceptions improperly configured" | removed import models from views.py                                                                                        | yes   |
| After creating order history template, receiving attribute error                                       | updated urls patterns functions in app urls.py                                                                             | Yes   |
| unable to open app in Heroku, application error                                                        | My Mentor Gareth Mckirr and wife Daisy McKirr kindly helped me resolve this issue by spending 2 hours to adjust my settings file and install Cloudinary | Yes   |My 
| email confirmation not received when order placed via Heroku site                                      | mail variables not declared in config vars settings in Heroku                                                              | Yes   |
| Few Cake Images not cropped and sized correctly                                     | Tried to adjust object-fit in styling properies used Adobe to resize but had an impact on site visibility. My primary focus was to ensure site has required functionality and output and authentications                                                            | No   |

# Future Enhancement

The site has room for improvement and additional functionality. In future, I would  propose to implement the following in future;

1. No search bar, cannot search products. I will consider implementing this for my next project.
2. More products and more categories on the site
3. Payment API, enabling customers to make a payment . I will consider this in my next project.

# Deployment

## Create PostgreSQL Database

1. Navigate to PostgreSQL from Code Institute template [CI PosgreSQL](https://dbs.ci-dbs.net/)
2. Enter your student email address in the input field provided.
3. Click Submit.
4. Wait while the database is created.
5. Your database is successfully created! Please review the email sent to your student email inbox.


## Heroku deployment

To deploy Mammas-Cakes to Heroku, take the following steps:
1. Create a requirements.txt file using the terminal command `pip freeze > requirements.txt`
2. Create a Procfile with the terminal command `echo web: python app.py > Procfile`. Ensure you use a capital 'P' for this file.
3. `git add` and `git commit` these changes and `git push` to GitHub repository
4. Go to the Heroku website and login. Create a new app by clicking the "New" button in your dashboard.
5. Give the app and name and set the region to Europe(or your closest region)
6. From the heroku dashboard of the new app, click on "Deploy" > "Deployment method" and select Github
7. Confirm the link to the correct GitHub repository- JModi16
8. In the heroku dashboard for the application. click on the "settings" > "Reveal Config Vars"
9. Set the following Config Vars:
   <img src="static/images/configvars.png"> database_url and secret key hidden to prevent security violation. Screenshot used from CI tutorial Codestar-blog walkthrough project.


10. In the Heroku dashboard, click "Deploy"
11. In the "Manual Deployment" section, ensure the master branch is selected then click "Deploy Branch"
11. The site is now deployed


# Credits

## Credits

   ### Content

- Code Institute was used throughout the tutorials enabling me to understand Python and Django, participating in the walthrough project enabled me to deliver my project.
- 
- Tutor at Bristol City College - Manuel Perez Romero for his great cooperation, advise and compassion due to my circumstances.

- Slack Community at Code Institute.

- Tutor support at Code Institute.


- [Crumbs and Dollies Cakes](https://www.crumbsanddoilies.co.uk/) to obtain amazing cake images.

   [Lolas Cakes](https://www.lolas.co.uk/)) to obtain spectacular cake images.

## Acknowledgements

-  My family for their patience whilst I learnt and completed this challenging project.
-  My brilliant mentor Gareth McGirr Daisy McGirr, for her excellent advice, reliable mentoring, going the extra mile.

