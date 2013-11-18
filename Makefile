.PHONY:	flex
	

flex:
	flex -+ dl.lex

flex-c:
	flex dl.lex
	
handin: *
	[ -f handin.tar.gz ] && rm handin.tar.gz || echo ""
	tar zcf handin.tar.gz *
