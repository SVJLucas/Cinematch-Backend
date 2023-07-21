from database.management import DatabaseManagement

# Object to be used by other files
database_management = dict()

database_management['admins'] = DatabaseManagement(table_name='Admins',
                                                   class_name_id='admin_id')

database_management['ais'] = DatabaseManagement(table_name='Ais',
                                                class_name_id='ai_id')

database_management['genres'] = DatabaseManagement(table_name='Genres',
                                                   class_name_id='genre_id')

database_management['movies'] = DatabaseManagement(table_name='Movies',
                                                   class_name_id='movie_id')

database_management['movies_genres'] = DatabaseManagement(table_name='MoviesGenres',
                                                          class_name_id='movie_genre_id')

database_management['ratings'] = DatabaseManagement(table_name='Ratings',
                                                    class_name_id='rating_id')

database_management['recommendations'] = DatabaseManagement(table_name='Recommendations',
                                                            class_name_id='recommendation_id')

database_management['users'] = DatabaseManagement(table_name='Users',
                                                  class_name_id='user_id')
