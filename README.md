# Introducing Cinematch: A Google Developers Student Club Initiative

<p align="center">
  <img width="500" alt="logo_dark_stacked_KzUurne (1)" src="https://github.com/SVJLucas/SVJLucas/assets/60625769/1501cb07-3add-4907-9778-10b90c223e69">
</p>

We're thrilled to introduce you to **Cinematch**, a project birthed in the collaborative environment of the Google Developers Student Club (GDSC). Our vision behind Cinematch was not just to revolutionize the movie recommendation domain, but to serve as a learning hub for students passionate about backend development.

By diving into the world of Cinematch, students will immerse themselves in a rich learning experience. Here's a curated list of skills and technologies you'll be exposed to as you navigate the construction and deployment of this project:

## Learning Outcomes:

1. **Backend Framework Familiarity**: Get hands-on experience with `FastAPI`, a modern Python framework known for its speedy performance and intuitive design.
2. **Python Mastery**: Refine your coding skills in Python, the language at the heart of Cinematch.
3. **API Development**: Understand the intricacies of designing a robust and efficient API, right from creating endpoints to handling various HTTP methods.
4. **Authentication and Security**: Dive deep into user authentication mechanisms, including session management and JWT token usage.
5. **Data Handling and Management**: Experience working with a comprehensive database, ensuring the proper management and retrieval of user data, movie information, and more.
6. **Deployment Skills**: Familiarize yourself with cloud-based deployments using `Google Cloud` and gain insights into platform-specific nuances.
7. **Firebase**: Explore the capabilities of Firebase, particularly for user management and authentication.
8. **Containerization with Docker**: Understand the importance of creating reproducible, scalable environments with Docker, ensuring consistent performance across different platforms.
9. **Database Design**: Grasp the principles of designing a relational database, from creating Entity-Relationship Models to understanding the significance of junction tables.
10. **Security Best Practices**: Embrace the importance of data security, learning techniques such as password hashing and secure data transmission.

Join us on this journey with Cinematch. Whether you're coding alongside or simply observing, we promise an enriching experience, packed with insights and learnings. The GDSC team believes in the transformative power of community-driven projects. Cinematch isn't just an API; it's a testament to what can be achieved when young developers come together with a shared vision.

Thank you for being a part of this mission. Here's to creating movie magic, one line of code at a time!




## Cinematch-Backend

![Concept Map of the Database](https://drive.google.com/uc?export=view&id=1Uw7pXNKox9uNbJWkQijx3-_3HY2BbQfE)

Welcome to the backend repository for Cinematch, a revolutionary movie recommendation platform! Cinematch is designed to connect users to movies they'll love but might not have discovered on their own.

## The API

The Cinematch API is a Python-based web service designed to serve the backend needs of the Cinematch movie recommendation platform. The API plays a pivotal role in handling user registration, authentication, and personalization, along with maintaining a comprehensive database of movies, user ratings, and recommendations.

### Web Service Architecture and Main Features
![Architectury](https://drive.google.com/uc?export=view&id=10oy-khllBvdljh5JrR7hRAqywdwPTtqd)

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

![Concept Map of the Database](https://drive.google.com/uc?export=view&id=1kZqGk2CQhsAXFeNpW0xjd5AiFj1aiDhB)

### Entity-Relationship Model

The Entity-Relationship Model provides a blueprint for an efficient database system that captures all necessary data and accurately defines relationships. It allows designers to manage user data, movie details, and ratings effectively.

![Concept Map of the Database](https://drive.google.com/uc?export=view&id=1pzLh18drRCEaANJ_iYQZ3dPsmiT7bq3m)

### Relational Database

The final database structure ensures that all essential data is accounted for, and relationships between entities are accurately defined, providing an efficient and organized system to manage user information, movie details, and user ratings effectively.

![Relational Database](https://drive.google.com/uc?export=view&id=1vhNdC_IRh40naBLLAn_003XbpNhdlp0V)

## Contact

If you have any questions, suggestions, or issues, please feel free to reach out.
Thank you for your interest in Cinematch. We can't wait to see the movie magic you'll create!
