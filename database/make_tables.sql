CREATE TABLE moderation
(
    id serial PRIMARY KEY,
    moderated_review text
);

CREATE TABLE reviews
(
    id serial PRIMARY KEY,
    review text
);

CREATE TABLE suggestions
(
    id serial PRIMARY KEY,
    suggestion text
);


