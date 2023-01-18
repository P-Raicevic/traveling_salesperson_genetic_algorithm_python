import random
import Chromosome as ch

# create a random chromosome --> shuffle node list randomly


def create_random_list(n_list):
    start = n_list[0]

    temp = n_list[1:]
    temp = random.sample(temp, len(temp))

    temp.insert(0, start)
    temp.append(start)
    return temp


# initialization
def initialization(data, pop_size):
    initial_population = []
    for i in range(0, pop_size):
        temp = create_random_list(data)
        new_ch = ch.Chromosome(temp)
        initial_population.append(new_ch)
    return initial_population

# crossover


def crossover_mix(p_1, p_2):
    point_1, point_2 = random.sample(range(1, len(p_1.chromosome)-1), 2)
    begin = min(point_1, point_2)
    end = max(point_1, point_2)

    child_1_1 = p_1.chromosome[:begin]
    child_1_2 = p_1.chromosome[end:]
    child_1 = child_1_1 + child_1_2
    child_2 = p_2.chromosome[begin:end+1]

    child_1_remain = [
        item for item in p_2.chromosome[1:-1] if item not in child_1]
    child_2_remain = [
        item for item in p_1.chromosome[1:-1] if item not in child_2]

    child_1 = child_1_1 + child_1_remain + child_1_2
    child_2 += child_2_remain

    child_2.insert(0, p_2.chromosome[0])
    child_2.append(p_2.chromosome[0])

    return child_1, child_2


# Mutation operation swap two nodes of the chromosome
def mutation(chromosome):
    mutation_index_1, mutation_index_2 = random.sample(
        range(1, len(chromosome)-1), 2)
    chromosome[mutation_index_1], chromosome[mutation_index_2] = chromosome[mutation_index_2], chromosome[mutation_index_1]
    return chromosome


# Find the best chromosome of the generation based on the cost
def find_best(generation):
    best = generation[0]
    for n in range(1, len(generation)):
        if generation[n].cost < best.cost:
            best = generation[n]
    return best

# select two chromosomes from a generation


def selection_pair(generation):
    return random.choices(
        generation,
        weights=[genome.fitness_value for genome in generation],
        k=2
    )


def create_new_generation(previous_generation, mutation_rate):

    for a in range(0, int(len(previous_generation)/2)):
        parents = selection_pair(previous_generation)

        parent_1 = parents[0]
        parent_2 = parents[1]
        new_generation = [find_best(previous_generation)]
        child_1, child_2 = crossover_mix(parent_1, parent_2)
        child_1 = ch.Chromosome(child_1)
        child_2 = ch.Chromosome(child_2)

        if random.random() < mutation_rate:
            mutated1 = mutation(child_1.chromosome)
            mutated2 = mutation(child_2.chromosome)
            child_1 = ch.Chromosome(mutated1)
            child_2 = ch.Chromosome(mutated2)

        new_generation.append(child_1)
        new_generation.append(child_2)

    return new_generation
