# Cinematch-Backend


![Concept Map of the Database](https://drive.google.com/uc?export=view&id=1HMVuoUZDbcMkdD-63Wc0Efh114SGs0s_)

Welcome to the backend repository for Cinematch, a revolutionary movie recommendation platform! Cinematch is designed to connect users to movies they'll love but might not have discovered on their own.

## Database's Design
### Concept map

A concept map in database design is a visual tool that depicts the relationships between different entities in a database. Using a concept map in the early stages of database design can help ensure that all necessary data is accounted for and that relationships between entities are correctly defined.

In this case, we focused in the main aspects:

* **Users**: They have attributes like Name, E-mail, and Password. The Password must be hashed for security reasons. Each user must have a unique identifier, which could be the E-mail.

* **Movies**: They have attributes like Title, Year, Mean Rating, Image URL, Synopsis, and Genres. Genres can have multiple values because a movie can belong to more than one genre.

* **Ratings**: This table could be a junction table that connects Users and Movies. It could include the User identifier, the Movie identifier, the Score that the user gave to the movie, and the Date/Time of the rating. The Score must be a number between 0 and 5.

![Concept Map of the Database](https://drive.google.com/uc?export=view&id=1kZqGk2CQhsAXFeNpW0xjd5AiFj1aiDhB)

## Contact

If you have any questions, suggestions, or issues, please feel free to reach out.
Thank you for your interest in Cinematch. We can't wait to see the movie magic you'll create!
