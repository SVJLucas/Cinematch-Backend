# Mastering Backend Development: A Workshop on Database Design to API Deployment

<p align="center">
  <img width="500" alt="logo_dark_stacked_KzUurne (1)" src="https://github.com/SVJLucas/SVJLucas/assets/60625769/1501cb07-3add-4907-9778-10b90c223e69">
</p>

Welcome to the **Cinematch Workshop**, organized by the Google Developers Student Club (GDSC). We are excited to have you join us for this in-depth, hands-on workshop where we will build and deploy the backend of a movie recommendation system. This session is designed to immerse you in backend development, equipping you with the skills and knowledge needed to bring robust applications to life.

Throughout this workshop, you’ll be working on the backend architecture of Cinematch, a project that will serve as a learning platform for understanding core backend technologies. We’ll guide you through the entire process, from setting up the environment to deploying the application on the cloud.

## What You'll Learn:

1. **Backend Framework Familiarity**: Get hands-on experience with `FastAPI`, a modern Python framework known for its speedy performance and intuitive design.
2. **Python Mastery**: Refine your coding skills in Python, the language at the heart of Cinematch.
3. **API Development**: Understand the intricacies of designing a robust and efficient API, from creating endpoints to handling various HTTP methods.
4. **Authentication and Security**: Dive deep into user authentication mechanisms, including session management and JWT token usage.
5. **Data Handling and Management**: Work with a comprehensive database, ensuring proper management and retrieval of user data, movie information, and more.
6. **Deployment Skills**: Familiarize yourself with cloud-based deployments using `Google Cloud` and gain insights into platform-specific nuances.
7. **Firebase Integration**: Explore the capabilities of Firebase, particularly for user management and authentication.
8. **Containerization with Docker**: Understand the importance of creating reproducible, scalable environments with Docker, ensuring consistent performance across different platforms.
9. **Database Design**: Grasp the principles of designing a relational database, from creating Entity-Relationship Models to understanding the significance of junction tables.
10. **Security Best Practices**: Embrace the importance of data security, learning techniques such as password hashing and secure data transmission.

Join us on this exciting journey as we build the backend of Cinematch. Whether you're coding alongside or following along, we promise an enriching experience packed with insights and practical knowledge. The GDSC team believes in the transformative power of community-driven projects. Cinematch is not just an API; it’s a testament to what can be achieved when passionate developers come together with a shared vision.

Thank you for being a part of this mission. Let's create movie magic, one line of code at a time!


## Cinematch-Backend

![Concept Map of the Database](https://drive.google.com/uc?export=view&id=1Uw7pXNKox9uNbJWkQijx3-_3HY2BbQfE)



Welcome to the backend repository for Cinematch, a revolutionary movie recommendation platform! Cinematch is designed to connect users to movies they'll love but might not have discovered on their own.

## The API

The Cinematch API is a Python-based web service designed to serve the backend needs of the Cinematch movie recommendation platform. The API plays a pivotal role in handling user registration, authentication, and personalization, along with maintaining a comprehensive database of movies, user ratings, and recommendations.

### Web Service Architecture and Main Features

<p align="center">
  <img width="700" alt="Architectury" src="https://github.com/user-attachments/assets/9c974f5c-0f30-4b94-bccf-78319bf0071d">
</p> 

Key Features:

 - **Management** : The API provides endpoints for user registration and login, effectively managing user authentication and session handling. It enables users to register and maintain profiles where they can view their activities, update their preferences, and manage personal information.

 - **Movie Management**: The API also keeps track of a vast catalog of movies, offering detailed information such as title, release year, average rating, image URL, synopsis, and genres. It provides endpoints to fetch individual movie details or lists of movies based on various filters.

 - **Ratings and Recommendations**: One of the core features of the API is its ability to record user ratings for movies and generate personalized movie recommendations. It uses a combination of these user ratings and advanced algorithms to offer suggestions tailored to the tastes of individual users.

 - **Data Security**: A top priority for the API is ensuring the safety of user data. Passwords are hashed before they are stored, and secure HTTP protocols are used for all data transmission, besides JWT tokens.

This API serves as the backbone of the Cinematch service, enabling movie enthusiasts to discover films they'll love but might not have found on their own.

## Documentation

For a more in-depth understanding of the API, including the details of its endpoints, request/response formats, and step-by-step guides on how to use them, refer to the official documentation **[here](https://cinematch-zb4scckqra-od.a.run.app/docs)** .

## Database's Design
### Concept map

A concept map in database design is a visual tool that depicts the relationships between different entities in a database. Using a concept map in the early stages of database design can help ensure that all necessary data is accounted for and that relationships between entities are correctly defined.

In this case, we focused in the main aspects:

* **Users**: They have attributes like Name, E-mail, and Password. The Password must be hashed for security reasons. Each user must have a unique identifier, which could be the E-mail.

* **Movies**: They have attributes like Title, Year, Mean Rating, Image URL, Synopsis, and Genres. Genres can have multiple values because a movie can belong to more than one genre.

* **Ratings**: This table could be a junction table that connects Users and Movies. It could include the User identifier, the Movie identifier, the Score that the user gave to the movie, and the Date/Time of the rating. The Score must be a number between 0 and 5.

<p align="center">
  <img width="700" alt="Database concept map" src="https://github.com/user-attachments/assets/1403c5ad-200d-4e0c-8eed-d0df2a68c808">
</p> 


### Entity-Relationship Model

The Entity-Relationship Model provides a blueprint for an efficient database system that captures all necessary data and accurately defines relationships. It allows designers to manage user data, movie details, and ratings effectively.

<p align="center">
  <img width="700" alt="Entity-Relationship Model" src="https://github.com/user-attachments/assets/1febfb63-8128-4d29-abaa-390a69dde773">
</p> 

### Relational Database

The final database structure ensures that all essential data is accounted for, and relationships between entities are accurately defined, providing an efficient and organized system to manage user information, movie details, and user ratings effectively.


<p align="center">
  <img width="700" alt="Relational Database" src="https://github.com/user-attachments/assets/509bb202-7801-4d0b-bec2-08022383e56d">
</p> 

## Contact

If you have any questions, suggestions, or issues, please feel free to reach out.
Thank you for your interest in Cinematch. We can't wait to see the movie magic you'll create!
