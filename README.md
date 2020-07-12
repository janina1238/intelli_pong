# Intelli Pong Umgebung

Umsetzung eines eigenen AI Pong Spiels:

Der Random Agent wurde auf dem rechten Paddle umgesetzt.
Der linke Paddle wird aktuell nur durch eine einfache Animation dargestellt.
Später wird die Animation durch den zweiten Agenten ersetzt.

Das Spiel wird beim ausführen der main.py gestartet.
Nach jeder Spielrunde wird der Reward der Runde zurückgegeben (Spielrunde wird beendet, wenn einer einen Score von 10 erreicht).
Wenn die Iteration beendet ist, wird ein gesamter Reward aller Spielrunden zurückgegeben.

# Agenten

Beide Agenten wurden mit dem Stable Baselines Framework trainiert.
Der rechte Paddle wurde mit dem PPO2 Algorithmus trainiert und musste gegen den animierten linken Paddle spielen.
Der linke Paddle wurde mit dem A2C Algorithmus trainiert und musste wiederum gegen das PPO2 Model spielen.
Da das Framework nach explizieten OpenAI Gym Methoden-Namen sucht (z.B. step()),
musste der erste Agent auf Replikate der Standard-Methoden verschoben werden (z.B. step_enemy()).
So kann der zweite Agent auf den Standard-Methoden trainiert werden und gegen das PPO2 Model spielen.
