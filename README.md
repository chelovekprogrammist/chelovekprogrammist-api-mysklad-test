# chelovekprogrammist-api-mysklad-test

Программа автоматизирует процесс создания заказов покупателя в сервисе Мой склад.
Программа ожидает PUSH уведомлений от озон, запрашивает данные о заказе и товаре
После создает по средствам API заказ покупателя в Сервисе мой склад

Запуск программы:
Для запуска приложения: flask run --host=0.0.0.0             # Этот способ не безопасный, и после закрытия терминала перестанет работать)
Для запуска приложения в фоновом режиме: nohup flask run &   # После выполнения этой команды, вы увидите PID процесса, например, [1] 1689. Это означает, что процесс был успешно запущен.
                                                             # Приложение будет работать в фоновом режиме, и все выводы будут записываться в файл nohup.out, который создастся в текущей директории. Если вы захотите остановить процесс, то для его завершения введите команду kill <PID> с указанием PID, который был выведен после запуска процесса.
sudo gunicorn app:app -c gunicorn_config.py                  # Правильный способ запуска приложения:


export FLASK_APP=app.py                                      # Чтобы не произошла ошибка лучше использовать при запуске эту строку
nohup sudo gunicorn app:app -c gunicorn_config.py &          # Правильный способ запуска приложения с функцией фонового режимв ЗАПУСКАТЬ ИЗ ПАПКИ С ПРИЛОЖЕНИЕМ app.py - Эта команда запустит процесс Gunicorn в фоновом режиме, используя файл конфигурации gunicorn_config.py, и сохранит вывод в файле nohup.out в текущей рабочей директории. Комбинация команды "nohup" и символа "&" позволяет запустить процесс в фоновом режиме и продолжить работу в терминале без блокировки.
											                              			    # Команда "sudo" используется для запуска процесса от имени суперпользователя, если требуется, чтобы процесс имел доступ к определенным системным ресурсам.
												                               			# Проверьте, что процесс запущен успешно, используя команду "ps aux | grep gunicorn". Вы должны увидеть процесс Gunicorn в выводе.
											                                 				# Чтобы остановить процесс, используйте команду "kill", например:
												                             	   		# sudo kill PID   или: sudo killall python3

											                           		 	    	# где "PID" - это идентификатор процесса, который можно получить из вывода команды "ps aux | grep gunicorn".               


Чтобы остановить автоматический запуск проекта при загрузке системы, вам нужно удалить файл службы, который вы создали ранее.
	

Для этого выполните следующие команды:

Остановите службу: sudo systemctl stop app.service
Отключите автозапуск службы:   sudo systemctl disable app.service
Удалите файл службы: sudo rm /etc/systemd/system/app.service
После выполнения этих команд служба myapp больше не будет запускаться автоматически при загрузке системы.

пути смены API:
'sudo systemctl edit myapp'
После этого нужно сохранить файл и перезапустить службу с помощью команды 'sudo systemctl restart myapp'
	
.bashrc  в корне приложения и в папке с приложением
