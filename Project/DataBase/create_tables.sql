CREATE TABLE Users (
    id SERIAL NOT NULL,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Courses (
    id SERIAL NOT NULL,
    name VARCHAR,
    title VARCHAR,
    owner_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES Users (id),
    students INT[],
    PRIMARY KEY (id)
);

CREATE TABLE Zapitu (
    id SERIAL NOT NULL,
    owner_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES Users (id),
    id_course INT NOT NULL,
    FOREIGN KEY (id_course) REFERENCES Courses (id),
    PRIMARY KEY (id)
);

