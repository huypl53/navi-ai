INSERT INTO
  `aes`.`mastery_bkt_multi_learn` (
    `user_id`,
    `skill_id`,
    `pl`,
    `updated_at`,
    `description`
  )
VALUES
  (
    2,
    10,
    0.5,
    '2024-06-30 16:30:30',
    'latest BKT multilearn'
  );

INSERT INTO
  `aes`.`bkt_params` (
    `create_at`,
    `modified_at`,
    `model_type`,
    `active`,
    `skill_id`,
    `ppl`,
    `ps`,
    `pt`,
    `pg`
  )
VALUES
  (
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    2,
    2,
    10,
    0.7,
    0.2,
    0.6,
    0.1
  );
