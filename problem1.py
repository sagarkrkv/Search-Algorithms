import itertools
###
#

# state: ()

'''
This program works by iterating items in five distinct positions in five distinct rows
   (people, package, received_package, place, should_go_place)

the goal state consists of distinct list which satisfies all the given constraints.
  
  state =  (	(people, package, received_package, place, should_go_place),
		(people, package, received_package, place, should_go_place),
		(people, package, received_package, place, should_go_place),
		(people, package, received_package, place, should_go_place),
		(people, package, received_package, place, should_go_place) )	

First we check the constraints the exist in the same row

   Universal Constraints    package != received_package
     			    place != should_go_place
			    No one received the correct package.

   Individual Constraints   1)The customer who ordered the Candelabrum received the Banister.
			    2)Frank received a Doorknob.
			    3)The delivery that should have gone to Kirkwood Street was sent to Lake Avenue.
			    4)Heather received the package that was to go to Orange Drive.
			    5)The Elephant arrived in North Avenue.
		            6)The customer on Maxwell Street received the Amplifier.

Now we check the constraints that exist across multiple rows 

   Constraints 	1)The customer who ordered the Banister received the package that Irene had ordered.
		2)George's package went to Kirkwood Street.
		3)The delivery that should have gone to Kirkwood Street was sent to Lake Avenue.
		4)Heather received the package that was to go to Orange Drive.
		5)Jerry received Heather order.
		6)The person who had ordered the ELEPHANT received the package that should have gone to Maxwell Street.
  
The we iterate over all possible states till we reach a state that satisfies all the constraints i.e goal state


'''

# (people, package, received_package, place, should_go_place)
#   0          1        2               3       4

people_list = ["Irene", "Frank", "George", "Heather", "Jerry"]
package_list = ["Candelabrum", "Banister", "Doorknob", "Elephant", "Amplifier"]
place_list = ["Kirkwood Street", "Lake Avenue", "Orange Drive", "North Avenue", "Maxwell Street"]

# choose two different item from list
# return all the possible tuples
# 
def _choose2(l):
    for i in l:
        for j in l:
            if i != j:
                yield (i, j)

#generates states
def state_generator():
    for package, received_package in _choose2(package_list):
        for place, should_go_place in _choose2(place_list):
            for people in people_list:
                yield (people, package, received_package, place, should_go_place)


#eliminates states that do not satisfy constraints in a single row using tuples
def goal_test_step1(state):
    people, package, received_package, place, should_go_place = state
    if package == received_package: return False
    if place == should_go_place: return False
    #The customer who ordered the Candelabrum received the Banister
    if package == "Candelabrum" and received_package != "Banister" \
        or package != "Candelabrum" and received_package == "Banister":
        return False
    #Frank received a Doorknob.
    if people == "Frank" and received_package != "Doorknob" \
        or people != "Frank" and received_package == "Doorknob":
        return False

    #The delivery that should have gone to Kirkwood Street was sent to Lake Avenue.
    
    if place == "Kirkwood Street" and should_go_place != "Lake Avenue" \
	or place != "Kirkwood Street" and should_go_place == "Lake Avenue": 
        return False


   # Heather received the package that was to go to Orange Drive
    if people == "Heather" and should_go_place != "Orange Drive" \
        or people != "Heather" and should_go_place == "Orange Drive":
        return False
    if people == "Heather" and place == "Orange Drive":
	return False
    
    #The Elephant arrived in North Avenue;
    if received_package == "Elephant" and place != "North Avenue" \
        or received_package != "Elephant" and place == "North Avenue":
        return False
    #No one received the correct package
    if package == "Elephant" and (should_go_place  == "North Avenue"\
	or place == "North Avenue" ) :
        return False

    #The customer on Maxwell Street received the Amplifier.
    if received_package == "Amplifier" and place != "Maxwell Street" \
        or received_package != "Amplifier" and place == "Maxwell Street":
        return False
    #No one received the correct package
    if package == "Amplifier" and (should_go_place == "Maxwell Street" \
	or place == "Maxwell Street") :
        return False
    
    

    return True


def find_state(index, value, states):
    return [state for state in states if state[index] == value][0]

def has_no_same(state1, state2):
    for index, item in enumerate(state1):
        if item == state2[index]:
            return False
    return True

def check_different(states):
    for i in range(5):
        # print states
        item_set = set(state[i] for state in states)
        if len(item_set) < 5:
            return False 
    return True

#eliminates states that do not satisfy constraints across multiple rows
def check_constrains(states):
    # the customer who ordered the Banister received 
    # the package that Irene had ordered
    ir = find_state(0, "Irene", states)
    b = find_state(1, "Banister", states)
    if b[2] != ir[1]:
         return False


    # George  package went to Kirkwood Street
    g = find_state(0, "George", states)
    ks = find_state(3, "Kirkwood Street", states)
    if g[1] != ks[2]:
        return False

    # The delivery that should
    # have gone to Kirkwood Street was sent to Lake Avenue. 
    la = find_state(3, "Lake Avenue", states)

    if la[2] != ks[1]:
        return False
    if la[4] != ks[3]:
	return False

    # Heather received the package that was to go to Orange Drive
    h = find_state(0, "Heather", states)
    od = find_state(3, "Orange Drive",states)
    if h[2] != od[1]:
         return False

    #Jerry received Heather order
    j = find_state(0, "Jerry", states)
    if h[1] != j[2]:
        return False

    # the person who had ordered the ELEPHANT received 
    # the package that should have gone to Maxwell Street.
    e = find_state(1, "Elephant", states)
    ms = find_state(3, "Maxwell Street", states)
    if e[2] != ms[1]:
        return False


    return True

if __name__ == "__main__":
    i = 1
    all_states = [state for state in state_generator() if goal_test_step1(state)]
    # print "all_states:%s"%len(all_states)
    # 286
    
    # while the customer who ordered the Banister received 
    # the package that Irene had ordered. ==
    possible_states = []
    for state1 in all_states:
        for state2 in all_states:
            if state1[0] == "Irene" and state2[1] == "Banister" \
                and state2[2] == state1[1]\
                and has_no_same(state1, state2):
                possible_states.append([state1, state2])
    # print "possible_states:%s"%len(possible_states)

    all_possible_states = []
    for states in possible_states:
        temp_states = [s for s in all_states if has_no_same(states[0], s)\
                                                and has_no_same(states[1], s)]
        for other_states in itertools.combinations(temp_states, 3):
            new_states = states + list(other_states)
            if check_different(new_states) and check_constrains(new_states):
                all_possible_states.append(new_states)

    print "there are %s solutions"%len(all_possible_states)

    for states in all_possible_states:
        print "======"
        i=1
        for state in states:
            print i,"%s ordered %s, but received %s, he/she lived in %s, the package he/she received should've been sent to %s."%state
            i+=1
	print "======"

