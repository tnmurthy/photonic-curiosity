"""
Multi-language localization support for Sudoku puzzles
Focus on Indian languages
"""

import json
import os
import random
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Localization:
    """Handle multi-language support for Sudoku puzzle generation."""
    
    # Indian languages configuration
    INDIAN_LANGUAGES = {
        'en': {'name': 'English', 'script': 'Latin'},
        'hi': {'name': 'Hindi', 'script': 'Devanagari'},
        'ta': {'name': 'Tamil', 'script': 'Tamil'},
        'te': {'name': 'Telugu', 'script': 'Telugu'},
        'bn': {'name': 'Bengali', 'script': 'Bengali'},
        'mr': {'name': 'Marathi', 'script': 'Devanagari'},
        'gu': {'name': 'Gujarati', 'script': 'Gujarati'},
        'kn': {'name': 'Kannada', 'script': 'Kannada'},
        'ml': {'name': 'Malayalam', 'script': 'Malayalam'},
        'pa': {'name': 'Punjabi', 'script': 'Gurmukhi'}
    }
    
    def __init__(self, locales_dir: str = 'locales'):
        """
        Initialize localization system.
        
        Args:
            locales_dir: Directory containing translation JSON files
        """
        self.locales_dir = locales_dir
        self.translations = {}
        self._load_all_translations()
    
    def _load_all_translations(self) -> None:
        """Load all available translation files."""
        if not os.path.exists(self.locales_dir):
            os.makedirs(self.locales_dir)
            logger.info(f"Created locales directory: {self.locales_dir}")
            return
        
        for lang_code in self.INDIAN_LANGUAGES.keys():
            self._load_translation(lang_code)
    
    def _load_translation(self, locale: str) -> None:
        """
        Load translations for a specific locale.
        
        Args:
            locale: Language code (e.g., 'hi', 'ta', 'en')
        """
        file_path = os.path.join(self.locales_dir, f"{locale}.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.translations[locale] = json.load(f)
                logger.info(f"Loaded translations for {locale}")
            except Exception as e:
                logger.error(f"Error loading {locale} translations: {e}")
                self.translations[locale] = self._get_default_translations(locale)
        else:
            # Create default translation file
            self.translations[locale] = self._get_default_translations(locale)
            self._save_translation(locale)
    
    def _get_default_translations(self, locale: str) -> Dict:
        """
        Get default translations for a locale.
        
        Args:
            locale: Language code
            
        Returns:
            Dict containing default translations
        """
        translations = {
            'en': {
                'difficulty': {
                    'easy': 'Easy',
                    'medium': 'Medium',
                    'hard': 'Hard',
                    'complex': 'Complex'
                },
                'ui': {
                    'daily_sudoku': 'Daily Sudoku',
                    'puzzle_number': 'Puzzle #{}',
                    'solution': 'Solution',
                    'challenge_yourself': 'Challenge Yourself!',
                    'enjoy': 'Enjoy!'
                },
                'captions': {
                    'templates': [
                        "🧩 Here is your {difficulty} Sudoku for today! How fast can you solve it? ⏱️\n\nSwipe for the solution! 👉\n\nPlay online: {website_url}\n\n",
                        "🧠 Time for a brain workout! A fresh {difficulty} Sudoku is here. Let us know your solve time in the comments! 👇\n\nPlay online: {website_url}\n\n",
                        "Calling all puzzle lovers! ✨ Your daily {difficulty} Sudoku has arrived. Can you conquer it?\n\nSwipe to see the answer! 👀\n\nPlay online: {website_url}\n\n",
                        "Ready, set, solve! 🚀 Here is a {difficulty} Sudoku to test your skills. Share your time below!\n\nPlay online: {website_url}\n\n"
                    ],
                    'call_to_action': "Follow us for more daily puzzles and brain teasers! 🤓"
                },
                'hashtags': {
                    'base': ['Sudoku', 'PuzzleOfTheDay', 'BrainTeaser', 'LogicPuzzle', 'MindGames', 
                             'PuzzleLovers', 'SudokuDaily', 'BrainTraining', 'NumberPuzzle', 'DailyChallenge', 'SudokuTime'],
                    'difficulty': {
                        'easy': ['EasySudoku', 'SudokuForBeginners', 'BeginnerPuzzle'],
                        'medium': ['MediumSudoku', 'SudokuChallenge'],
                        'hard': ['HardSudoku', 'ExpertSudoku', 'SudokuMaster']
                    }
                }
            },
            'hi': {
                'difficulty': {
                    'easy': 'आसान',
                    'medium': 'मध्यम',
                    'hard': 'कठिन',
                    'complex': 'जटिल'
                },
                'ui': {
                    'daily_sudoku': 'दैनिक सुडोकु',
                    'puzzle_number': 'पहेली #{}',
                    'solution': 'समाधान',
                    'challenge_yourself': 'खुद को चुनौती दें!',
                    'enjoy': 'आनंद लें!'
                },
                'captions': {
                    'template': "🧩 {} सुडोकु चुनौती!\n\nआज की पहेली के साथ अपने तर्क और समस्या-समाधान कौशल का परीक्षण करें।\n\n💡 समाधान देखने के लिए स्वाइप करें!\n\n",
                    'call_to_action': 'क्या आप इसे हल कर सकते हैं? टिप्पणियों में अपना समय साझा करें! ⏱️'
                },
                'hashtags': {
                    'base': ['सुडोकु', 'पहेली', 'दिमागीखेल', 'तर्कपहेली', 'Sudoku', 'PuzzleOfTheDay', 
                            'IndianPuzzles', 'HindiSudoku', 'BrainGames', 'DailyChallenge'],
                    'difficulty': {
                        'easy': ['आसानसुडोकु', 'शुरुआतीपहेली'],
                        'medium': ['मध्यमसुडोकु'],
                        'hard': ['कठिनसुडोकु', 'चुनौतीपूर्ण']
                    }
                }
            },
            'ta': {
                'difficulty': {
                    'easy': 'எளிதானது',
                    'medium': 'நடுத்தர',
                    'hard': 'கடினமானது',
                    'complex': 'சிக்கலானது'
                },
                'ui': {
                    'daily_sudoku': 'தினசரி சுடோகு',
                    'puzzle_number': 'புதிர் #{}',
                    'solution': 'தீர்வு',
                    'challenge_yourself': 'உங்களை சவால் செய்யுங்கள்!',
                    'enjoy': 'மகிழுங்கள்!'
                },
                'captions': {
                    'template': "🧩 {} சுடோகு சவால்!\n\nஇன்றைய புதிருடன் உங்கள் தர்க்கம் மற்றும் சிக்கல் தீர்க்கும் திறன்களை சோதிக்கவும்.\n\n💡 தீர்வைக் காண ஸ்வைப் செய்யவும்!\n\n",
                    'call_to_action': 'நீங்கள் இதை தீர்க்க முடியுமா? கருத்துகளில் உங்கள் நேரத்தை பகிரவும்! ⏱️'
                },
                'hashtags': {
                    'base': ['சுடோகு', 'புதிர்', 'Sudoku', 'TamilSudoku', 'PuzzleOfTheDay', 
                            'TamilPuzzles', 'BrainGames', 'LogicPuzzle'],
                    'difficulty': {
                        'easy': ['எளிதானசுடோகு'],
                        'medium': ['நடுத்தரசுடோகு'],
                        'hard': ['கடினமானசுடோகு']
                    }
                }
            },
            'te': {
                'difficulty': {
                    'easy': 'సులభం',
                    'medium': 'మధ్యస్థం',
                    'hard': 'కష్టం',
                    'complex': 'సంక్లిష్టం'
                },
                'ui': {
                    'daily_sudoku': 'రోజువారీ సుడోకు',
                    'puzzle_number': 'పజిల్ #{}',
                    'solution': 'పరిష్కారం',
                    'challenge_yourself': 'మిమ్మల్ని మీరు సవాలు చేయండి!',
                    'enjoy': 'ఆనందించండి!'
                },
                'captions': {
                    'template': "🧩 {} సుడోకు ఛాలెంజ్!\n\nఈ రోజు పజిల్‌తో మీ తార్కికత మరియు సమస్య పరిష్కార నైపుణ్యాలను పరీక్షించండి.\n\n💡 పరిష్కారం చూడటానికి స్వైప్ చేయండి!\n\n",
                    'call_to_action': 'మీరు దీన్ని పరిష్కరించగలరా? వ్యాఖ్యలలో మీ సమయాన్ని భాగస్వామ్యం చేయండి! ⏱️'
                },
                'hashtags': {
                    'base': ['సుడోకు', 'పజిల్', 'Sudoku', 'TeluguSudoku', 'PuzzleOfTheDay', 
                            'TeluguPuzzles', 'BrainGames'],
                    'difficulty': {
                        'easy': ['సులభసుడోకు'],
                        'medium': ['మధ్యస్థసుడోకు'],
                        'hard': ['కష్టసుడోకు']
                    }
                }
            },
            'bn': {
                'difficulty': {
                    'easy': 'সহজ',
                    'medium': 'মাঝারি',
                    'hard': 'কঠিন',
                    'complex': 'জটিল'
                },
                'ui': {
                    'daily_sudoku': 'দৈনিক সুডোকু',
                    'puzzle_number': 'ধাঁধা #{}',
                    'solution': 'সমাধান',
                    'challenge_yourself': 'নিজেকে চ্যালেঞ্জ করুন!',
                    'enjoy': 'উপভোগ করুন!'
                },
                'captions': {
                    'template': "🧩 {} সুডোকু চ্যালেঞ্জ!\n\nআজকের ধাঁধা দিয়ে আপনার যুক্তি এবং সমস্যা সমাধানের দক্ষতা পরীক্ষা করুন।\n\n💡 সমাধান দেখতে স্বাইপ করুন!\n\n",
                    'call_to_action': 'আপনি কি এটি সমাধান করতে পারবেন? মন্তব্যে আপনার সময় শেয়ার করুন! ⏱️'
                },
                'hashtags': {
                    'base': ['সুডোকু', 'ধাঁধা', 'Sudoku', 'BengaliSudoku', 'PuzzleOfTheDay', 
                            'BengaliPuzzles', 'BrainGames'],
                    'difficulty': {
                        'easy': ['সহজসুডোকু'],
                        'medium': ['মাঝারিসুডোকু'],
                        'hard': ['কঠিনসুডোকু']
                    }
                }
            },
            'mr': {
                'difficulty': {
                    'easy': 'सोपे',
                    'medium': 'मध्यम',
                    'hard': 'कठीण',
                    'complex': 'गुंतागुंतीचे'
                },
                'ui': {
                    'daily_sudoku': 'दैनिक सुडोकू',
                    'puzzle_number': 'कोडे #{}',
                    'solution': 'उपाय',
                    'challenge_yourself': 'स्वतःला आव्हान द्या!',
                    'enjoy': 'आनंद घ्या!'
                },
                'captions': {
                    'template': "🧩 {} सुडोकू आव्हान!\n\nआजच्या कोड्यासह तुमचे तर्क आणि समस्या सोडवण्याचे कौशल्य तपासा.\n\n💡 उपाय पाहण्यासाठी स्वाइप करा!\n\n",
                    'call_to_action': 'तुम्ही हे सोडवू शकता का? टिप्पण्यांमध्ये तुमचा वेळ शेअर करा! ⏱️'
                },
                'hashtags': {
                    'base': ['सुडोकू', 'कोडे', 'Sudoku', 'MarathiSudoku', 'PuzzleOfTheDay', 
                            'MarathiPuzzles', 'BrainGames'],
                    'difficulty': {
                        'easy': ['सोपेसुडोकू'],
                        'medium': ['मध्यमसुडोकू'],
                        'hard': ['कठीणसुडोकू']
                    }
                }
            },
            'gu': {
                'difficulty': {
                    'easy': 'સરળ',
                    'medium': 'મધ્યમ',
                    'hard': 'મુશ્કેલ',
                    'complex': 'જટિલ'
                },
                'ui': {
                    'daily_sudoku': 'દૈનિક સુડોકુ',
                    'puzzle_number': 'પઝલ #{}',
                    'solution': 'ઉકેલ',
                    'challenge_yourself': 'તમારી જાતને પડકાર આપો!',
                    'enjoy': 'આનંદ માણો!'
                },
                'captions': {
                    'template': "🧩 {} સુડોકુ પડકાર!\n\nઆજની પઝલ સાથે તમારી તર્ક અને સમસ્યા હલ કરવાની કુશળતા ચકાસો.\n\n💡 ઉકેલ જોવા માટે સ્વાઇપ કરો!\n\n",
                    'call_to_action': 'શું તમે આને ઉકેલી શકો છો? ટિપ્પણીઓમાં તમારો સમય શેર કરો! ⏱️'
                },
                'hashtags': {
                    'base': ['સુડોકુ', 'પઝલ', 'Sudoku', 'GujaratiSudoku', 'PuzzleOfTheDay', 
                            'GujaratiPuzzles', 'BrainGames'],
                    'difficulty': {
                        'easy': ['સરળસુડોકુ'],
                        'medium': ['મધ્યમસુડોકુ'],
                        'hard': ['મુશ્કેલસુડોકુ']
                    }
                }
            },
            'kn': {
                'difficulty': {
                    'easy': 'ಸುಲಭ',
                    'medium': 'ಮಧ್ಯಮ',
                    'hard': 'ಕಠಿಣ',
                    'complex': 'ಸಂಕೀರ್ಣ'
                },
                'ui': {
                    'daily_sudoku': 'ದೈನಂದಿನ ಸುಡೋಕು',
                    'puzzle_number': 'ಒಗಟು #{}',
                    'solution': 'ಪರಿಹಾರ',
                    'challenge_yourself': 'ನಿಮ್ಮನ್ನು ಸವಾಲು ಮಾಡಿ!',
                    'enjoy': 'ಆನಂದಿಸಿ!'
                },
                'captions': {
                    'template': "🧩 {} ಸುಡೋಕು ಸವಾಲು!\n\nಇಂದಿನ ಒಗಟಿನೊಂದಿಗೆ ನಿಮ್ಮ ತರ್ಕ ಮತ್ತು ಸಮಸ್ಯೆ ಪರಿಹಾರ ಕೌಶಲ್ಯಗಳನ್ನು ಪರೀಕ್ಷಿಸಿ.\n\n💡 ಪರಿಹಾರವನ್ನು ನೋಡಲು ಸ್ವೈಪ್ ಮಾಡಿ!\n\n",
                    'call_to_action': 'ನೀವು ಇದನ್ನು ಪರಿಹರಿಸಬಹುದೇ? ಕಾಮೆಂಟ್‌ಗಳಲ್ಲಿ ನಿಮ್ಮ ಸಮಯವನ್ನು ಹಂಚಿಕೊಳ್ಳಿ! ⏱️'
                },
                'hashtags': {
                    'base': ['ಸುಡೋಕು', 'ಒಗಟು', 'Sudoku', 'KannadaSudoku', 'PuzzleOfTheDay', 
                            'KannadaPuzzles', 'BrainGames'],
                    'difficulty': {
                        'easy': ['ಸುಲಭಸುಡೋಕು'],
                        'medium': ['ಮಧ್ಯಮಸುಡೋಕು'],
                        'hard': ['ಕಠಿಣಸುಡೋಕು']
                    }
                }
            },
            'ml': {
                'difficulty': {
                    'easy': 'എളുപ്പം',
                    'medium': 'ഇടത്തരം',
                    'hard': 'ബുദ്ധിമുട്ട്',
                    'complex': 'സങ്കീർണ്ണം'
                },
                'ui': {
                    'daily_sudoku': 'ദിനംപ്രതി സുഡോകു',
                    'puzzle_number': 'പസിൽ #{}',
                    'solution': 'പരിഹാരം',
                    'challenge_yourself': 'സ്വയം വെല്ലുവിളിക്കൂ!',
                    'enjoy': 'ആസ്വദിക്കൂ!'
                },
                'captions': {
                    'template': "🧩 {} സുഡോകു വെല്ലുവിളി!\n\nഇന്നത്തെ പസിൽ ഉപയോഗിച്ച് നിങ്ങളുടെ യുക്തിയും പ്രശ്നപരിഹാര കഴിവുകളും പരീക്ഷിക്കൂ.\n\n💡 പരിഹാരം കാണാൻ സ്വൈപ്പ് ചെയ്യൂ!\n\n",
                    'call_to_action': 'നിങ്ങൾക്ക് ഇത് പരിഹരിക്കാൻ കഴിയുമോ? കമന്റുകളിൽ നിങ്ങളുടെ സമയം പങ്കിടൂ! ⏱️'
                },
                'hashtags': {
                    'base': ['സുഡോകു', 'പസിൽ', 'Sudoku', 'MalayalamSudoku', 'PuzzleOfTheDay', 
                            'MalayalamPuzzles', 'BrainGames'],
                    'difficulty': {
                        'easy': ['എളുപ്പംസുഡോകു'],
                        'medium': ['ഇടത്തരംസുഡോകു'],
                        'hard': ['ബുദ്ധിമുട്ട്സുഡോകു']
                    }
                }
            },
            'pa': {
                'difficulty': {
                    'easy': 'ਸੌਖਾ',
                    'medium': 'ਮੱਧਮ',
                    'hard': 'ਔਖਾ',
                    'complex': 'ਗੁੰਝਲਦਾਰ'
                },
                'ui': {
                    'daily_sudoku': 'ਰੋਜ਼ਾਨਾ ਸੁਡੋਕੂ',
                    'puzzle_number': 'ਬੁਝਾਰਤ #{}',
                    'solution': 'ਹੱਲ',
                    'challenge_yourself': 'ਆਪਣੇ ਆਪ ਨੂੰ ਚੁਣੌਤੀ ਦਿਓ!',
                    'enjoy': 'ਲੁਫਤ ਉਠਾਓ!'
                },
                'captions': {
                    'template': "🧩 {} ਸੁਡੋਕੂ ਚੁਣੌਤੀ!\n\nਅੱਜ ਦੀ ਬੁਝਾਰਤ ਨਾਲ ਆਪਣੀ ਤਰਕ ਅਤੇ ਸਮੱਸਿਆ ਹੱਲ ਕਰਨ ਦੀ ਯੋਗਤਾ ਦੀ ਜਾਂਚ ਕਰੋ.\n\n💡 ਹੱਲ ਵੇਖਣ ਲਈ ਸਵਾਈਪ ਕਰੋ!\n\n",
                    'call_to_action': 'ਕੀ ਤੁਸੀਂ ਇਸ ਨੂੰ ਹੱਲ ਕਰ ਸਕਦੇ ਹੋ? ਟਿੱਪਣੀਆਂ ਵਿੱਚ ਆਪਣਾ ਸਮਾਂ ਸਾਂਝਾ ਕਰੋ! ⏱️'
                },
                'hashtags': {
                    'base': ['ਸੁਡੋਕੂ', 'ਬੁਝਾਰਤ', 'Sudoku', 'PunjabiSudoku', 'PuzzleOfTheDay', 
                            'PunjabiPuzzles', 'BrainGames'],
                    'difficulty': {
                        'easy': ['ਸੌਖਾਸੁਡੋਕੂ'],
                        'medium': ['ਮੱਧਮਸੁਡੋਕੂ'],
                        'hard': ['ਔਖਾਸੁਡੋਕੂ']
                    }
                }
            }
        }
        
        return translations.get(locale, translations['en'])
    
    def _save_translation(self, locale: str) -> None:
        """Save translation to JSON file."""
        file_path = os.path.join(self.locales_dir, f"{locale}.json")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.translations[locale], f, ensure_ascii=False, indent=2)
            logger.info(f"Saved translations for {locale}")
        except Exception as e:
            logger.error(f"Error saving {locale} translations: {e}")
    
    def get_text(self, locale: str, key_path: str, default: str = '') -> str:
        """
        Get translated text for a specific key path.
        
        Args:
            locale: Language code
            key_path: Dot-separated path to translation key (e.g., 'ui.daily_sudoku')
            default: Default value if key not found
            
        Returns:
            Translated text
        """
        if locale not in self.translations:
            locale = 'en'
        
        keys = key_path.split('.')
        value = self.translations[locale]
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value if isinstance(value, str) else default
    
    def get_hashtags(self, locale: str, difficulty: str) -> List[str]:
        """
        Get hashtags for a specific locale and difficulty.
        
        Args:
            locale: Language code
            difficulty: Difficulty level
            
        Returns:
            List of hashtags
        """
        base_tags = self.get_text(locale, 'hashtags.base', [])
        diff_tags = self.get_text(locale, f'hashtags.difficulty.{difficulty}', [])
        
        # Combine and return (limit to 30 tags for Instagram)
        all_tags = base_tags + diff_tags
        return all_tags[:30]
    
    def format_caption(self, locale: str, difficulty: str, website_url: str) -> str:
        """
        Generate a complete caption for a puzzle post.
        
        Args:
            locale: Language code
            difficulty: Difficulty level
            website_url: URL to the website
            
        Returns:
            Formatted caption with hashtags
        """
        difficulty_text = self.get_text(locale, f'difficulty.{difficulty}', difficulty.title())

        # Get caption templates and choose one at random
        templates = self.get_text(locale, 'captions.templates', [])
        if not templates:
            # Fallback for older translation files
            templates = [self.get_text(locale, 'captions.template', "🧩 {difficulty} Sudoku Challenge!")]

        template = random.choice(templates)

        # Get call to action
        cta = self.get_text(locale, 'captions.call_to_action', '')
        
        # Format caption
        caption = template.format(difficulty=difficulty_text, website_url=website_url) + cta
        
        # Add hashtags
        hashtags = self.get_hashtags(locale, difficulty)
        hashtag_string = ' '.join([f'#{tag}' for tag in hashtags])
        
        return f"{caption}\n\n{hashtag_string}"


if __name__ == "__main__":
    # Test localization
    loc = Localization()
    
    print("Testing Indian Language Support:")
    print("=" * 60)
    
    for lang_code, lang_info in loc.INDIAN_LANGUAGES.items():
        print(f"\n{lang_info['name']} ({lang_code}):")
        print(f"  Script: {lang_info['script']}")
        print(f"  Daily Sudoku: {loc.get_text(lang_code, 'ui.daily_sudoku')}")
        print(f"  Easy: {loc.get_text(lang_code,'difficulty.easy')}")
        print(f"  Hashtags: {', '.join(loc.get_hashtags(lang_code, 'easy')[:5])}...")
