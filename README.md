# Cinematch-Backend


![Concept Map of the Database](https://drive.google.com/uc?export=view&id=1Uw7pXNKox9uNbJWkQijx3-_3HY2BbQfE)

Welcome to the backend repository for Cinematch, a revolutionary movie recommendation platform! Cinematch is designed to connect users to movies they'll love but might not have discovered on their own.

## The API

The Cinematch API is a Python-based web service designed to serve the backend needs of the Cinematch movie recommendation platform. The API plays a pivotal role in handling user registration, authentication, and personalization, along with maintaining a comprehensive database of movies, user ratings, and recommendations.

### Architectury and Features
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

### Relational Database

The final structure for the database was this:

![Relational Database](https://drive.google.com/uc?export=view&id=1vhNdC_IRh40naBLLAn_003XbpNhdlp0V)

## Contact

If you have any questions, suggestions, or issues, please feel free to reach out.
Thank you for your interest in Cinematch. We can't wait to see the movie magic you'll create!
