import unittest
from application import *

class TestRemoveArticle(unittest.TestCase):

	def test_remove_a(self):
		self.assertEqual(remove_articles('a','a'), 'a')
		self.assertEqual(remove_articles('a time to kill','a time to kill'), 'a time to kill')
		self.assertEqual(remove_articles('a time to kill','time to kill'), 'time to kill')
	def test_remove_the(self):
		self.assertEqual(remove_articles('the','the'), 'the')
		self.assertEqual(remove_articles('the game','the game'), 'the game')
		self.assertEqual(remove_articles('the game','game'), 'game')
	def test_remove_an(self):
		self.assertEqual(remove_articles('an','an'), 'an')
		self.assertEqual(remove_articles('an education','an education'), 'an education')
		self.assertEqual(remove_articles('an education','education'), 'education')
	def test_start_with_the(self):
		self.assertEqual(remove_articles('theory of everything','the imatation game'), 'theory of everything')
		self.assertEqual(remove_articles('theory of everything','theory of everything'), 'theory of everything')
	def test_empty(self):	
		self.assertEqual(remove_articles('',''), '')
		
	def test_different_articles(self):
		self.assertEqual(remove_articles('the dark knight','a dark knight'), 'dark knight')


class TestCountDifferences(unittest.TestCase):
	def test_empty(self):
		self.assertEqual(count_differences('',''), [0])
	def test_one_word_same_len(self):
		self.assertEqual(count_differences('a','b'), [1])

		self.assertEqual(count_differences('ab','aa'), [1])
		self.assertEqual(count_differences('ab','ba'), [2])
		self.assertEqual(count_differences('ab','cd'),[2])
		self.assertEqual(count_differences('ab','bb'),[1])

		self.assertEqual(count_differences('abc','abd'),[1])
		self.assertEqual(count_differences('abc','acc'),[1])
		self.assertEqual(count_differences('abc','bbc'),[1])
		self.assertEqual(count_differences('abc','cba'),[2])
		self.assertEqual(count_differences('abc','cab'),[3])

		self.assertEqual(count_differences('imitation','imatation'),[1])


	def test_one_word_diff_len(self):
		self.assertEqual(count_differences('a',''),[1])
		self.assertEqual(count_differences('a','aa'),[1])
		self.assertEqual(count_differences('ab','a'),[1])
		self.assertEqual(count_differences('a','ba'),[2])

		self.assertEqual(count_differences('abc','bc'),[3])
		self.assertEqual(count_differences('abc','b'),[3])
		self.assertEqual(count_differences('abc','a'),[2])
		self.assertEqual(count_differences('','b'),[1])
		self.assertEqual(count_differences('','bc'),[2])
		self.assertEqual(count_differences('imitation','imitate'),[3])
		self.assertEqual(count_differences('imitation','inception'),[4])
		self.assertEqual(count_differences('imitation','mitation'),[9])


	def test_multi_word(self):
		self.assertEqual(count_differences('a b','a a'),[0,1])

		self.assertEqual(count_differences('a b c','a b b'),[0,0,1])
		self.assertEqual(count_differences('a b c','b b b'),[1,0,1])

		self.assertEqual(count_differences('once upon a time in america',\
			'once upon a time in hollywood'),[0,0,0,0,0,9])
		self.assertEqual(count_differences('once upon a time in hollywood',\
			'once upon a time in america'),[0,0,0,0,0,9])
		self.assertEqual(count_differences('once upon a time in america',\
			'once up on a time in hollywood'),[0,2,1,4,2,16])
		self.assertEqual(count_differences('once upon a time in america',\
			'onceuponatimeinamerica'),[0,0,0,0,0,0])

		self.assertEqual(count_differences('once upon a time in the west',\
			'once upon a time in west'),[0,0,0,0,0,3,4])

	def test_ignore_symbols(self):
		self.assertEqual(count_differences('pride & predjudice',\
			'pride and predjudice'),[0,0,0])
		self.assertEqual(count_differences("molly's game",\
			"mollys game"),[0,0])
		self.assertEqual(count_differences("moulin rouge!",\
			"moulin rouge"),[0,0])
		self.assertEqual(count_differences("the cabinet of dr. caligari",\
			"the cabinet of dr caligari"),[0,0,0,0,0])

	def test_one_word_no_diffs(self):
		self.assertEqual(count_differences('ab','ab'), [0])
		self.assertEqual(count_differences('a','a'), [0])
		self.assertEqual(count_differences('abc','abc'), [0])
		self.assertEqual(count_differences('abcdef','abcdef'), [0])
		self.assertEqual(count_differences('abcdef','abcdef'), [0])
	def test_multi_words_no_diffs(self):
		self.assertEqual(count_differences('crimson peak','crimson peak'), [0,0])
		self.assertEqual(count_differences('zero dark thirty','zero dark thirty'), [0,0,0])

		self.assertEqual(count_differences('a a','a a'),[0,0])

		self.assertEqual(count_differences('a b c','a b c'),[0,0,0])
		self.assertEqual(count_differences('a b b','a b b'),[0,0,0])

class TestCloseEnough(unittest.TestCase):
	def test_same_titles(self):
		self.assertTrue(close_enough('crimson peak','crimson peak'))
	def test_one_difference(self):
		self.assertTrue(close_enough('crimson peak','crimson peek'))
		self.assertTrue(close_enough('crimson peak','crimson beak'))
		self.assertTrue(close_enough('crimson peak','crimsom peak'))
		self.assertTrue(close_enough('crimson peak','trimson peak'))
	def test_upto_3_diffs(self):
		self.assertTrue(close_enough('crimson peak','crinson peek'))
		self.assertTrue(close_enough('crimson peak','crinsom peek'))
		self.assertTrue(close_enough('inception','incettion'))
	def test_more_correct_words(self):
		self.assertTrue(close_enough('it\'s always sunny in philadelphia','its always suny in philidelphia'))
		self.assertTrue(close_enough('murder on the orient express',\
			'muder on the orient express'))

	def test_missing_article(self):
		self.assertTrue(close_enough('the favourite','favourite'))
		self.assertTrue(close_enough('an education','education'))
		self.assertTrue(close_enough('a serious man','serious man'))
	def test_long_words_correct(self):
		self.assertTrue(close_enough('once upon a time in america',\
			'onse upon a time im america'))
		self.assertTrue(close_enough('fantastic beasts and where to find them',\
			'fantastic beasts an were to find them'))
		self.assertTrue(close_enough('murder on the orient express',\
			'murder on the orien express'))


	def test_same_len_diff_titles(self):
		self.assertFalse(close_enough('crimson tide','crinsom peak'))
		self.assertFalse(close_enough('once upon a time in america',\
			'once upon a time in hollywood'))
		self.assertFalse(close_enough('once upon a time in hollywood',\
			'once upon a time in america'))
		self.assertFalse(close_enough('mirror mirror',\
			'magic mike'))
		self.assertFalse(close_enough('inception',\
			'insomnia'))

	def test_diff_len_diff_titles(self):
		self.assertFalse(close_enough('once upon a time in the west',\
			'once up on a time in hollywood'))
		self.assertFalse(close_enough('once upon a time in america',\
			'once up on a time in the west'))
		self.assertFalse(close_enough('proof','proof of life'))
		self.assertFalse(close_enough('an unfinished life','proof of life'))
		self.assertFalse(close_enough('an unfinished life','life'))


if __name__ == '__main__':
	unittest.main()