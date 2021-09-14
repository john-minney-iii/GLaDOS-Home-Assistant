
from gladosTTS import GLaDOSTTS

def main() -> None:
    gladosTTS = GLaDOSTTS()
    gladosTTS.play_file('oh-its-you.wav')
    # gladosTTS.play_file('oh-its-you')
    # gladosTTS.play_file('biggest-lesson')
    # gladosTTS.play_file('biggest-lesson-2')

if __name__ == "__main__":
    main()