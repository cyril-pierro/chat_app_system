SET 'auto.offset.reset'='earliest';
create stream users_stream with (kafka_topic='users_topic.public.users',value_format='avro');
create stream created_users_stream with (kafka_topic='created_users',value_format='json') as select after->id as user_id, after->username as username,after->email as email, after->hash_password as password, after->is_a_star as star, after->is_admin as is_admin, after->is_email_verified as is_email_verified, after->joined_at as joined_at from users_stream where op in ('c', 'u');
create stream elastic_users_stream with (kafka_topic='elasticsearch_users', value_format='json') as select user_id, username, star from created_users_stream where is_email_verified = true;

select * from ELASTIC_USERS_STREAM emit changes;
