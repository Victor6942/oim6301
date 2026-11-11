# TV Show ERD

```mermaid
erDiagram
    SHOWS ||--o{ EPISODES : "has"
    SHOWS ||--o{ CAST_ROLES : "has"
    PEOPLE ||--o{ CAST_ROLES : "plays"

    SHOWS {
        int show_id PK
        string title
        int first_year
    }
    EPISODES {
        int episode_id PK
        int show_id FK
        int season
        int episode_number
        string title
        date air_date
    }
    PEOPLE {
        int person_id PK
        string name
    }
    CAST_ROLES {
        int show_id PK, FK
        int person_id PK, FK
        string character_name
    }
```

## How to read it

- A show has zero or more episodes. An episode belongs to exactly one show.
- A show has many actors and an actor is in many shows, so `cast_roles` sits in the middle. Its two keys together are its primary key.