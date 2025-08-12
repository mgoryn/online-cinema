language_schema_example = {"id": 1, "name": "English"}

country_schema_example = {"id": 1, "code": "US", "name": "United States"}

genre_schema_example = {"id": 1, "name": "Drama"}

actor_schema_example = {"id": 1, "name": "Tom Hanks"}

# --- Examples for Movie Schemas ---

movie_item_schema_example = {
    "id": 1,
    "name": "Forrest Gump",
    "date": "1994-07-06",
    "score": 88.0,
    "overview": "The presidencies of Kennedy and Johnson, the Vietnam War,"
    " the Watergate scandal and other historical events unfold"
    " from the perspective of an Alabama man with an IQ of 75,"
    " whose only desire is to be reunited with his childhood sweetheart.",
}

movie_list_response_schema_example = {
    "movies": [
        movie_item_schema_example,
        {
            "id": 2,
            "name": "The Green Mile",
            "date": "1999-12-10",
            "score": 86.0,
            "overview": "The lives of guards on Death Row are affected by one of their charges:"
            " a black man accused of child murder and rape, yet who has a mysterious gift.",
        },
    ],
    "prev_page": "/api/v1/theater/movies?page=1&size=2",
    "next_page": "/api/v1/theater/movies?page=3&size=2",
    "total_pages": 50,
    "total_items": 100,
}

movie_create_schema_example = {
    "name": "The Great Adventure",
    "date": "2025-10-01",
    "score": 75.0,
    "overview": "An epic journey of a young explorer.",
    "status": "In Production",
    "budget": 150000000.00,
    "revenue": 0.00,
    "country": "US",
    "genres": ["Adventure", "Action"],
    "actors": ["Chris Pratt", "Zoe Saldana"],
    "languages": ["English"],
}

movie_detail_schema_example = {
    "id": 1,
    "name": "Forrest Gump",
    "date": "1994-07-06",
    "score": 88.0,
    "overview": "The presidencies of Kennedy and Johnson, the Vietnam War,"
    " the Watergate scandal and other historical events unfold from"
    " the perspective of an Alabama man with an IQ of 75, whose only"
    " desire is to be reunited with his childhood sweetheart.",
    "status": "Released",
    "budget": 55000000.00,
    "revenue": 677945399.00,
    "country": country_schema_example,
    "genres": [genre_schema_example, {"id": 2, "name": "Romance"}],
    "actors": [actor_schema_example],
    "languages": [language_schema_example],
}

movie_update_schema_example = {
    "score": 89.0,
    "overview": "An updated and more detailed overview of the movie.",
}
