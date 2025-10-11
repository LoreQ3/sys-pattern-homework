# Домашнее задание к занятию "Расширенные возможности SQL" студента Аль-Ассафа Ильи»

---

Задание можно выполнить как в любом IDE, так и в командной строке.

### Задание 1

Одним запросом получите информацию о магазине, в котором обслуживается более 300 покупателей, и выведите в результат следующую информацию: 
- фамилия и имя сотрудника из этого магазина;
- город нахождения магазина;
- количество пользователей, закреплённых в этом магазине.

```sql
SELECT 
    CONCAT(staff.first_name, ' ', staff.last_name) AS staff_name,
    city.city AS store_city,
    COUNT(customer.customer_id) AS customer_count
FROM store
    INNER JOIN staff ON store.manager_staff_id = staff.staff_id
    INNER JOIN address ON store.address_id = address.address_id
    INNER JOIN city ON address.city_id = city.city_id
    INNER JOIN customer ON store.store_id = customer.store_id
GROUP BY 
    store.store_id, 
    staff.first_name, 
    staff.last_name, 
    city.city
HAVING COUNT(customer.customer_id) > 300;
```

### Задание 2

Получите количество фильмов, продолжительность которых больше средней продолжительности всех фильмов.

```sql
SELECT COUNT(*) AS films_above_average
FROM film
WHERE length > (SELECT AVG(length) FROM film);
```

### Задание 3

Получите информацию, за какой месяц была получена наибольшая сумма платежей, и добавьте информацию по количеству аренд за этот месяц.

```sql
USE sakila;
SELECT 
    DATE_FORMAT(payment_date, '%Y-%m') AS payment_month,
    SUM(amount) AS total_amount,
    COUNT(rental_id) AS rental_count
FROM payment
GROUP BY DATE_FORMAT(payment_date, '%Y-%m')
ORDER BY total_amount DESC
LIMIT 1;
```

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### Задание 4*

Посчитайте количество продаж, выполненных каждым продавцом. Добавьте вычисляемую колонку «Премия». Если количество продаж превышает 8000, то значение в колонке будет «Да», иначе должно быть значение «Нет».

### Задание 5*

Найдите фильмы, которые ни разу не брали в аренду.

```sql
USE sakila;
SELECT 
    f.film_id,
    f.title,
    f.release_year,
    f.length,
    f.rating,
    f.rental_rate
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
LEFT JOIN rental r ON i.inventory_id = r.inventory_id
WHERE r.rental_id IS NULL
ORDER BY f.title;
```
