# Домашнее задание к занятию  «Очереди RabbitMQ» студента Аль-Ассафа Ильи

### Задание 1. Установка RabbitMQ

Используя Vagrant или VirtualBox, создайте виртуальную машину и установите RabbitMQ.
Добавьте management plug-in и зайдите в веб-интерфейс.

*Итогом выполнения домашнего задания будет приложенный скриншот веб-интерфейса RabbitMQ.*
![Скриншот](https://github.com/LoreQ3/sys-pattern-homework/blob/main/img/img1.png)

---

### Задание 2. Отправка и получение сообщений

Используя приложенные скрипты, проведите тестовую отправку и получение сообщения.
Для отправки сообщений необходимо запустить скрипт producer.py.

Для работы скриптов вам необходимо установить Python версии 3 и библиотеку Pika.
Также в скриптах нужно указать IP-адрес машины, на которой запущен RabbitMQ, заменив localhost на нужный IP.

```shell script
$ pip install pika
```

Зайдите в веб-интерфейс, найдите очередь под названием hello и сделайте скриншот.
После чего запустите второй скрипт consumer.py и сделайте скриншот результата выполнения скрипта

*В качестве решения домашнего задания приложите оба скриншота, сделанных на этапе выполнения.*

Для закрепления материала можете попробовать модифицировать скрипты, чтобы поменять название очереди и отправляемое сообщение.

![Скриншот](https://github.com/LoreQ3/sys-pattern-homework/blob/main/img/img2.png)
![Скриншот](https://github.com/LoreQ3/sys-pattern-homework/blob/main/img/img3.png)
![Скриншот](https://github.com/LoreQ3/sys-pattern-homework/blob/main/img/img4.png)

---

### Задание 3. Подготовка HA кластера

Используя Vagrant или VirtualBox, создайте вторую виртуальную машину и установите RabbitMQ.
Добавьте в файл hosts название и IP-адрес каждой машины, чтобы машины могли видеть друг друга по имени.

Пример содержимого hosts файла:
```shell script
$ cat /etc/hosts
192.168.0.10 rmq01
192.168.0.11 rmq02
```
После этого ваши машины могут пинговаться по имени.

Затем объедините две машины в кластер и создайте политику ha-all на все очереди.

*В качестве решения домашнего задания приложите скриншоты из веб-интерфейса с информацией о доступных нодах в кластере и включённой политикой.*
![Скриншот](https://github.com/LoreQ3/sys-pattern-homework/blob/main/img/img1.png)

Также приложите вывод команды с двух нод:

```shell script
$ rabbitmqctl cluster_status
```

Для закрепления материала снова запустите скрипт producer.py и приложите скриншот выполнения команды на каждой из нод:

```shell script
$ rabbitmqadmin get queue='hello'
```

После чего попробуйте отключить одну из нод, желательно ту, к которой подключались из скрипта, затем поправьте параметры подключения в скрипте consumer.py на вторую ноду и запустите его.

*Приложите скриншот результата работы второго скрипта.*
![Скриншот](https://github.com/LoreQ3/sys-pattern-homework/blob/main/img/img5.png)
![Скриншот](https://github.com/LoreQ3/sys-pattern-homework/blob/main/img/img6.png)
![Скриншот](https://github.com/LoreQ3/sys-pattern-homework/blob/main/img/img7.png)
![Скриншот](https://github.com/LoreQ3/sys-pattern-homework/blob/main/img/img8.png)

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### * Задание 4. Ansible playbook

Напишите плейбук, который будет производить установку RabbitMQ на любое количество нод и объединять их в кластер.
При этом будет автоматически создавать политику ha-all.

*Готовый плейбук разместите в своём репозитории.*

```hcl
---
- name: Deploy RabbitMQ HA Cluster
  hosts: all
  become: yes
  vars:
    rabbitmq_cluster_nodes: "{{ groups['rabbitmq'] | map('extract', hostvars, ['ansible_host']) | list }}"
    rabbitmq_erlang_cookie: "SECRET_CLUSTER_COOKIE"
  
  tasks:
    - name: Install RabbitMQ
      apt:
        name: rabbitmq-server
        state: present
        update_cache: yes
      when: ansible_os_family == "Debian"
    
    - name: Enable management plugin
      command: rabbitmq-plugins enable rabbitmq_management
      notify: restart rabbitmq
    
    - name: Configure Erlang cookie
      copy:
        content: "{{ rabbitmq_erlang_cookie }}"
        dest: /var/lib/rabbitmq/.erlang.cookie
        owner: rabbitmq
        group: rabbitmq
        mode: '0400'
      notify: restart rabbitmq
    
    - name: Start RabbitMQ service
      systemd:
        name: rabbitmq-server
        state: started
        enabled: yes
    
    - name: Create admin user
      command: "rabbitmqctl add_user admin password"
      ignore_errors: yes
    
    - name: Set admin permissions
      command: "rabbitmqctl set_user_tags admin administrator"
    
    - name: Set admin permissions
      command: "rabbitmqctl set_permissions -p / admin '.*' '.*' '.*'"
  
  handlers:
    - name: restart rabbitmq
      systemd:
        name: rabbitmq-server
        state: restarted

- name: Configure RabbitMQ cluster
  hosts: rabbitmq
  become: yes
  tasks:
    - name: Join cluster with first node
      command: >
        rabbitmqctl stop_app &&
        rabbitmqctl reset &&
        rabbitmqctl join_cluster rabbit@{{ groups['rabbitmq'][0] }} &&
        rabbitmqctl start_app
      when: inventory_hostname != groups['rabbitmq'][0]
    
    - name: Set HA policy
      command: rabbitmqctl set_policy ha-all ".*" '{"ha-mode":"all"}'
      when: inventory_hostname == groups['rabbitmq'][0]

```
