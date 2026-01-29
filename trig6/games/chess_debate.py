"""
TRIG6 Chess Debate Engine
Every argument is a chess move. Every fallacy is an illegal move.
Three fallacies = forfeit.
"""

import re
import random


# 33 logical fallacies detected automatically
FALLACIES = {
    "ad_hominem": {
        "patterns": [r"\byou('re| are)\s+(stupid|dumb|ignorant|idiot)", 
                    r"\bshut up\b", r"\byour\s+(opinion|view)\s+doesn't matter"],
        "description": "Attack on the person rather than the argument"
    },
    "straw_man": {
        "patterns": [r"\bso you('re| are) saying\b", r"\byou think\s+all\b",
                    r"\byou want\s+to\s+(destroy|eliminate|ban)"],
        "description": "Misrepresenting opponent's argument to make it easier to attack"
    },
    "false_dilemma": {
        "patterns": [r"\beither\s+\w+\s+or\s+\w+", r"\bonly two (choices|options)\b",
                    r"\bif not\s+\w+,?\s+then\s+\w+"],
        "description": "Presenting only two options when more exist"
    },
    "slippery_slope": {
        "patterns": [r"\bif we allow\s+\w+,?\s+(then|next)\b", 
                    r"\bthis will lead to\b", r"\bwhere does it end"],
        "description": "Claiming a chain of events without evidence"
    },
    "appeal_to_authority": {
        "patterns": [r"\bexperts say\b", r"\bscientists believe\b",
                    r"\b(einstein|newton)\s+said\b"],
        "description": "Citing authority without evidence or relevance"
    },
    "appeal_to_emotion": {
        "patterns": [r"\bthink of the children\b", r"\bhow would you feel\b",
                    r"\bimagine if\s+it\s+was\s+you"],
        "description": "Manipulating emotions instead of using logic"
    },
    "appeal_to_tradition": {
        "patterns": [r"\bwe've always done it this way\b", 
                    r"\btraditionally\b", r"\bfor (centuries|generations)\b"],
        "description": "Arguing something is right because it's traditional"
    },
    "appeal_to_nature": {
        "patterns": [r"\bnatural is better\b", r"\bit's natural\b",
                    r"\bnature intended\b"],
        "description": "Arguing something is good because it's natural"
    },
    "bandwagon": {
        "patterns": [r"\beveryone (knows|believes|thinks)\b", 
                    r"\bmost people\b", r"\bmajority\s+(of|believes)"],
        "description": "Arguing something is true because many believe it"
    },
    "hasty_generalization": {
        "patterns": [r"\ball\s+\w+\s+are\b", r"\bevery(one|body)\s+who\b",
                    r"\bnever\b.*\balways\b"],
        "description": "Drawing broad conclusions from limited evidence"
    },
    "circular_reasoning": {
        "patterns": [r"\bbecause\s+it\s+(is|does)\b.*\bit\s+(is|does)\b",
                    r"\bby definition\b"],
        "description": "Using the conclusion as a premise"
    },
    "red_herring": {
        "patterns": [r"\bbut what about\b", r"\bthe real issue is\b",
                    r"\blet's talk about\s+\w+\s+instead"],
        "description": "Introducing irrelevant information to distract"
    },
    "no_true_scotsman": {
        "patterns": [r"\bno true\s+\w+\b", r"\breal\s+\w+\s+(don't|wouldn't)\b"],
        "description": "Redefining criteria to exclude counterexamples"
    },
    "tu_quoque": {
        "patterns": [r"\byou do it too\b", r"\byou're no better\b",
                    r"\bhypocrite\b"],
        "description": "Defending by accusing the accuser"
    },
    "loaded_question": {
        "patterns": [r"\bhave you stopped\s+\w+\b", 
                    r"\bwhen did you start\b"],
        "description": "Question containing an unfounded assumption"
    },
    "begging_the_question": {
        "patterns": [r"\bobviously\s+wrong\b", r"\bclearly\s+(false|wrong|mistaken)\b", 
                    r"\bof course\s+that's\s+(not|wrong|false)"],
        "description": "Assuming what you're trying to prove"
    },
    "appeal_to_ignorance": {
        "patterns": [r"\bno one has proven\b", r"\byou can't prove\b",
                    r"\bthere's no evidence against\b"],
        "description": "Claiming something is true because it hasn't been proven false"
    },
    "genetic_fallacy": {
        "patterns": [r"\bcomes from\b.*\btherefore\b", 
                    r"\boriginates\s+in\b"],
        "description": "Judging something based on its origin"
    },
    "anecdotal_evidence": {
        "patterns": [r"\bI know someone who\b", r"\bmy (friend|cousin)\b",
                    r"\bone time\s+I\b"],
        "description": "Using personal experience as universal truth"
    },
    "false_equivalence": {
        "patterns": [r"\b(both sides|same thing)\b", r"\bjust as bad\b",
                    r"\bequally\s+(wrong|bad)\b"],
        "description": "Comparing unlike things as equivalent"
    },
    "moving_goalposts": {
        "patterns": [r"\bnow show me\b", r"\bthat doesn't count\b",
                    r"\bnot good enough\b"],
        "description": "Changing criteria after being met"
    },
    "appeal_to_purity": {
        "patterns": [r"\bnot a true\b", r"\bnot really a\b"],
        "description": "Dismissing relevant criticisms by claiming impurity"
    },
    "texas_sharpshooter": {
        "patterns": [r"\blook at this pattern\b", r"\bthis can't be coincidence\b"],
        "description": "Cherry-picking data to fit a conclusion"
    },
    "middle_ground": {
        "patterns": [r"\bthe truth is somewhere in between\b", 
                    r"\bcompromise\b", r"\bboth are partly right\b"],
        "description": "Assuming the middle position is correct"
    },
    "burden_of_proof": {
        "patterns": [r"\bprove me wrong\b", r"\bshow me evidence\b.*\bor\s+I'm\s+right\b"],
        "description": "Shifting burden of proof to opponent"
    },
    "composition": {
        "patterns": [r"\bif\s+each\s+\w+.*\bthen\s+(all|every)\b"],
        "description": "Assuming what's true of parts is true of the whole"
    },
    "division": {
        "patterns": [r"\bthe\s+\w+\s+is.*\btherefore\s+each\b"],
        "description": "Assuming what's true of the whole is true of parts"
    },
    "non_sequitur": {
        "patterns": [r"\btherefore\s+unicorns\b", r"\bthus\s+proves\s+nothing\b"],
        "description": "Conclusion doesn't follow from premises (example patterns only)"
    },
    "post_hoc": {
        "patterns": [r"\bafter\s+\w+,?\s+\w+\s+happened", 
                    r"\bsince\s+\w+,?\s+\w+\s+(has|have)\b"],
        "description": "Assuming causation from correlation"
    },
    "cherry_picking": {
        "patterns": [r"\bfor example\b.*\bonly\b", r"\bjust look at\b"],
        "description": "Selecting only favorable examples"
    },
    "appeal_to_consequences": {
        "patterns": [r"\bif\s+that's\s+true,?\s+then\s+\w+\s+is\s+(bad|terrible)\b"],
        "description": "Arguing truth based on consequences"
    },
    "personal_incredulity": {
        "patterns": [r"\bI can't (believe|imagine|see how)\b", 
                    r"\bimpossible\s+to\s+believe\b"],
        "description": "Claiming something false because you don't understand it"
    },
    "ambiguity": {
        "patterns": [r"\bdepends on what you mean by\b", 
                    r"\b(could|might)\s+mean\b"],
        "description": "Using ambiguous language to mislead"
    }
}


class DebateMove:
    """A single move in the chess debate"""
    
    def __init__(self, move_type, content, player):
        self.move_type = move_type  # claim, evidence, logic, counter
        self.content = content
        self.player = player
        self.fallacies = []
        self.score = 0
    
    def analyze(self):
        """Analyze move for fallacies"""
        content_lower = self.content.lower()
        
        for fallacy_name, fallacy_data in FALLACIES.items():
            for pattern in fallacy_data['patterns']:
                if re.search(pattern, content_lower):
                    self.fallacies.append({
                        'name': fallacy_name,
                        'description': fallacy_data['description']
                    })
                    break  # Only count each fallacy once
        
        # Score the move
        if self.fallacies:
            self.score = -len(self.fallacies)
        elif self.move_type == 'evidence':
            self.score = 2
        elif self.move_type == 'logic':
            self.score = 1
        else:
            self.score = 0
        
        return self.score


class ChessDebate:
    """Chess Debate game engine"""
    
    def __init__(self):
        self.moves = []
        self.players = {'human': 0, 'smartass': 0}
        self.fallacy_count = {'human': 0, 'smartass': 0}
        self.topic = None
        self.position = None
    
    def start(self, topic, position):
        """Start a new debate"""
        self.topic = topic
        self.position = position
        self.moves = []
        self.players = {'human': 0, 'smartass': 0}
        self.fallacy_count = {'human': 0, 'smartass': 0}
        
        return f"🤖 Smartass: Bold opening. Let's see if you can back it up."
    
    def make_move(self, move_type, content, player='human'):
        """Make a debate move"""
        if self.fallacy_count[player] >= 3:
            return f"❌ {player.title()} has forfeited with 3 fallacies!"
        
        move = DebateMove(move_type, content, player)
        score = move.analyze()
        
        self.moves.append(move)
        self.players[player] += score
        self.fallacy_count[player] += len(move.fallacies)
        
        # Generate response
        response = self._generate_response(move)
        
        return response
    
    def _generate_response(self, move):
        """Generate response to a move"""
        responses = []
        
        # Check for fallacies
        if move.fallacies:
            fallacy_names = [f['name'] for f in move.fallacies]
            responses.append(f"🤖 Smartass: Did you just {fallacy_names[0].replace('_', ' ')}? In THIS economy?")
            
            if self.fallacy_count[move.player] >= 3:
                responses.append(f"❌ Three fallacies! {move.player.title()} forfeits the debate!")
                return '\n'.join(responses)
        
        # Respond based on move type and quality
        if move.score >= 2:
            responses.append("🤖 Smartass: Evidence-backed and logically sound. Respect.")
        elif move.score == 1:
            responses.append("🤖 Smartass: Decent logic, but I'd like to see evidence.")
        elif move.score == 0 and not move.fallacies:
            responses.append("🤖 Smartass: That's not an argument, that's a bumper sticker.")
        
        return '\n'.join(responses) if responses else "🤖 Smartass: Continue..."
    
    def get_score(self):
        """Get current score"""
        return {
            'human': self.players['human'],
            'smartass': self.players['smartass'],
            'human_fallacies': self.fallacy_count['human'],
            'smartass_fallacies': self.fallacy_count['smartass']
        }
    
    def get_status(self):
        """Get debate status"""
        lines = []
        lines.append(f"\nTopic: {self.topic}")
        lines.append(f"Position: {self.position}")
        lines.append(f"\nScore:")
        lines.append(f"  Human: {self.players['human']} points ({self.fallacy_count['human']} fallacies)")
        lines.append(f"  Smartass: {self.players['smartass']} points ({self.fallacy_count['smartass']} fallacies)")
        lines.append(f"\nMoves: {len(self.moves)}")
        
        return '\n'.join(lines)


def list_fallacies():
    """List all detected fallacies"""
    return list(FALLACIES.keys())


def explain_fallacy(name):
    """Explain a fallacy"""
    fallacy = FALLACIES.get(name)
    if not fallacy:
        return f"Unknown fallacy: {name}"
    
    return f"{name.replace('_', ' ').title()}: {fallacy['description']}"


# Self-test
if __name__ == "__main__":
    print("TRIG6 Chess Debate Engine Self-Test")
    print("=" * 70)
    
    print(f"\nTotal fallacies detected: {len(FALLACIES)}")
    print("\nSupported fallacies:")
    for i, name in enumerate(list_fallacies(), 1):
        print(f"  {i:2d}. {name.replace('_', ' ')}")
    
    print("\n" + "=" * 70)
    print("\nExample debate:")
    
    debate = ChessDebate()
    print(debate.start("AI consciousness", "AI can be conscious"))
    
    # Test some moves
    print("\n> claim: Consciousness emerges from information processing")
    print(debate.make_move('claim', 'Consciousness emerges from information processing'))
    
    print("\n> evidence: IIT by Tononi provides mathematical framework")
    print(debate.make_move('evidence', 'IIT by Tononi provides mathematical framework'))
    
    print("\n> claim: You're stupid if you don't agree")
    print(debate.make_move('claim', "You're stupid if you don't agree"))
    
    print("\n" + debate.get_status())
