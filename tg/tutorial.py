from pong import Game 
import pygame
import neat
import os
import pickle 
class Pongame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.rigt_padle = self.game.right_paddle
        self.left_paddle = self.game.left_paddle
        self.ball = self.game.ball

    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        run = True 
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left= True, up=True)
            elif keys[pygame.K_s]:
                self.game.move_paddle(left= True, up=False)
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()

            output = net.activate((self.rigt_padle.y, self.ball.y, abs(self.rigt_padle.x - self.ball.x)))

            decision = output.index(max(output))
            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_paddle(left=False, up=True)
            elif decision == 2:
                self.game.move_paddle(left=False, up=False)

            

            game_info = self.game.loop()
            print(F"left hit: {game_info.left_hits} \n left score: {game_info.left_score} \n right hit: {game_info.right_hits} \n right score: {game_info.right_score} \n ")
            self.game.draw()
            pygame.display.update()

        pygame.quit()
#en son buradayd ım

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                
            outpu1 =  net1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            decision1 = outpu1.index(max(outpu1))
            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.move_paddle(left=True, up=True)
            elif decision1 == 2:
                self.game.move_paddle(left=True, up=False)
            output2 = net2.activate((self.rigt_padle.y, self.ball.y, abs(self.rigt_padle.x -self.ball.x)))
            decision2 = output2.index(max(output2))
            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.move_paddle(left=False, up=True)
            elif decision2 == 2:
                self.game.move_paddle(left=False, up=False)
            game_info = self.game.loop()
            self.game.draw( draw_hits=True, draw_score=True)
            pygame.display.update()
            if game_info.left_score >= 1 or game_info.right_score >= 1 or game_info.left_hits >= 10 or game_info.right_hits >= 50:
                break
    def calculate_fitness(self, genome1, genome2, game_info):
        genome1.fitness += game_info.left_hits
        genome2.fitness += game_info.right_hits


def eval_genomes(genomes, config):
    width = 700
    height = 500
    
    window = pygame.display.set_mode((width, height))

    for i, (genome_id1, genome1) in enumerate(genomes):
        if(i == len(genomes)-1):
            break 
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
            game = Pongame(window, width, height)
            game.train_ai(genome1, genome2, config)


def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)
    with open("best.pkl", "wb") as f:
        pickle.dump(winner, f)

def test_ai(config):
    width = 700
    height = 500
    window = pygame.display.set_mode((width, height))
    with open("winnet.pkl", "rb") as f:
        winner = pickle.load(f)
    game = Pongame(window, width, height)
    game.test_ai(winner)




if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    #run_neat(config)
    test_ai(config)