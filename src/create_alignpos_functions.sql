DELIMITER //
CREATE FUNCTION `nextval`(`seq_name` varchar(100))
RETURNS varchar(100) CHARSET utf8
BEGIN
    DECLARE cur_val INT;
DECLARE prefix_val varchar(100);
    SELECT
        cur_value, prefix INTO cur_val, prefix_val
    FROM
        tabSequence
    WHERE
        name = seq_name; 
    IF cur_val IS NOT NULL THEN
        UPDATE
            tabSequence
        SET
            cur_value = IF (
                (cur_value + increment) > max_value OR (cur_value + increment) < min_value,
                IF (
                    cycle = TRUE,
                    IF (
                        (cur_value + increment) > max_value,
                        min_value, 
                        max_value 
                    ),
                    NULL
                ),
                cur_value + increment
            )
        WHERE
            name = seq_name;
    END IF;
IF prefix_val IS NOT NULL THEN
RETURN concat(prefix_val, lpad(cur_val,5,0));
ELSE
RETURN lpad(cur_val,5,0);
END IF;

END; //

DELIMITER ;
