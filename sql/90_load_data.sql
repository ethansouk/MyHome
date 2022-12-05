set session my.number_of_samples = '100';

-- Filling of products
--INSERT INTO sample
--select id, concat('Sample_', id) 
--FROM GENERATE_SERIES(1, current_setting('my.number_of_samples')::int) as id;