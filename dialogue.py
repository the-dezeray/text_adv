n =[None]*100

n[0] =msg(msg ="Welcome, traveler. What brings you to these ancient woods",
	responces =
	[
		responce(
			msg = "Cautiously: I seek answers, guidance... something to make sense of the turmoil in my heart.",
			go_to =1
			),

		responce(
			msg ="Confidently: I'm here to explore, to unravel the mysteries hidden within these woods",
			go_to =2)
	]
	)

n[2] =msg("well in a few days uou wont be",
	responces=
	[
		responce(
			msg ="why do you say so",
			go_to =3
			),

		responce("i am of steel",4)
	]
	)


n[2] =msg("well in a few days uou wont be",
	responces=
	[
		responce(
			msg ="engage combat",

			func = (enter_combat),
			argument = "python 1"
			)

		
	]
	)