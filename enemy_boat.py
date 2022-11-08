from pygame.math import Vector2
import pygame
import random
import pickle
import math

from pathfind_node import PathfindNode
from boat import Boat, BoatImage
from cannon import Cannon
import settings
import tools

class EnemyBoat(Boat):
    """boat with enemy behaviour"""
    def __init__(self, groups: list[pygame.sprite.Group], start_pos: tuple, 
                 start_hp: float, start_damage: float, start_speed: float):
        super().__init__(groups, start_pos)
        self.z = 0

        # STATS
        self.start_hp = start_hp
        self.hp = start_hp
        self.damage = start_damage
        self.speed = start_speed
        self.max_speed = start_speed # speed of boat when moving normally
        
        self.state = "following"                         # current state the enemy is in (following/shooting)

        # add variation so enemies will be shooting from different distances
        self.shoot_variation = random.randint(-100, 100)
        self.shoot_distance = settings.ENEMY_SHOOT_DISTANCE + self.shoot_variation

        self.cannons.append(Cannon(self, (0,45), True, None, self.damage, "enemy"))
        self.get_sails()
        self.images = [self.hull] + self.cannons + self.sails # all boat images to be used to compile main image
        self.make_main_boat_image()

        self.shoot_timer = 0 # counts down to 0 when the enemy's shooting for enemy to shoot cannon

        self.pathfinded = False # tracks whether the enemy has pathfinded to the player

    def get_sails(self) -> None:
        """get all enemy boat sail images"""
        self.main_sail = BoatImage("main_sail_black.png", (0,-10))
        self.nest = BoatImage("nest.png", (0,self.main_sail.centre_offset.y-23))
        self.flag = BoatImage("flag_black.png", (0,self.nest.centre_offset.y-10))
        self.small_sail = BoatImage("small_sail_black.png", (0,31))
        self.sails = [self.main_sail, self.nest, self.flag, self.small_sail]
    
    def update(self) -> None:
        """called once per frame"""
        self.states()
        if self.state == "following":
            self.pathfind()
            self.check_new_pathfind()
            self.update_current_path_step()
            self.adjust_angle()
        if self.state == "shooting":
            self.try_shoot()
        
        self.check_despawn()
        
        # FOR DEBUGGING
        # for path_pos in self.path:
        #     rect = pygame.Rect(path_pos*settings.PIECE_SIZE, (settings.PIECE_SIZE, settings.PIECE_SIZE))
        #     rect.topleft += settings.current_run.camera.camera_move
        #     pygame.draw.circle(pygame.display.get_surface(), "red", rect.center, 5)
        # pygame.draw.circle(pygame.display.get_surface(), "blue", self.pos + settings.current_run.camera.camera_move,
        #                    settings.ENEMY_NEXT_STEP_DISTANCE, width=2)
        # pygame.draw.circle(pygame.display.get_surface(), "green", self.current_path_pos + settings.current_run.camera.camera_move, 5)
        # pygame.draw.line(pygame.display.get_surface(), "green",  self.pos + settings.current_run.camera.camera_move, 
        #                    self.current_path_pos + settings.current_run.camera.camera_move, 2)

        super().update()
    
    def states(self) -> None:
        """changes the state of the enemy boat"""
        # if the boat is too far away from the player to shoot
        if abs(self.pos.distance_to(settings.current_run.player_boat.pos)) > self.shoot_distance:
            self.state = "following"

            # if self.speed < settings.BOAT_BASE_SPEED: # needs to slow down
            #     self.speed += settings.ENEMY_ACCELERATION * 1/tools.get_fps() # increase speed
            #     self.speed = min(self.speed, settings.BOAT_BASE_SPEED)        # limit maximum
        else:
            self.state = "shooting"

            if self.speed > 0: # needs to speed up
                self.speed -= settings.ENEMY_ACCELERATION * 1/tools.get_fps() # decrease speed
                self.speed = max(self.speed, 0)                               # limit mimimum
    
    def check_new_pathfind(self) -> None:
        """checks if the enemy should pathfind again"""
        if not self.pathfinded: return # already able to pathfind

        # player's current position is out of radius of old pathfinded position
        if settings.current_run.player_boat.pos.distance_to(self.old_player_position) > settings.ENEMY_NEW_PATH_RADIUS:
            self.pathfinded = False # pathfind again
    
    def pathfind(self) -> None:
        """pathfinds towards the player if it needs to"""
        if self.pathfinded: return # don't pathfind if it already has
        
        self.nodes = pickle.loads(settings.current_run.base_nodes) # make personal copy of nodes to edit
        self.get_node_positions()
        
        for node in self.nodes: # calculate the heuristics for all the nodes
            node.calculate_heuristic(self.target_node.pos)
        
        # CALCULATE AND GET PATH
        self.pathfind_calculate()
        self.path = self.get_path(self.target_node) 

        # FINISH PATHFINDING AND START FOLLOWING IT
        self.pathfinded = True
        self.old_player_position = settings.current_run.player_boat.rect.center # player position when pathfinding happened
        self.current_path_step = len(self.path)-1 # current step of path to travel to
        self.current_path_pos = self.pos # start at position
        self.update_current_path_step()

        # angle correctly at start of path following
        target_angle = math.atan2(self.current_path_pos.x-self.pos.x, self.current_path_pos.y-self.pos.y)
        self.angle = target_angle*(180/math.pi) + 180

    def get_node_positions(self) -> None:
        """get the node positions of the enemy and player boat"""
        # current position of enemy boat in normalised map
        self.map_pos = self.pos // settings.PIECE_SIZE
        for node in self.nodes: # find the current map node
            if node.pos == self.map_pos: 
                self.current_node = node
                break
        else: 
            self.current_node = PathfindNode(self.map_pos) # make sure the current position is a node even if it's not traversable
            self.nodes.append(self.current_node)
        
        # set up current node
        self.current_node.distance_from_start = 0
        self.current_node.total_distance = 0
        
        player = settings.current_run.player_boat # store player for easy access
        # current position of player in normalised map
        self.player_map_pos = player.pos // settings.PIECE_SIZE
        for node in self.nodes: # find the target node
            if node.pos == self.player_map_pos:
                self.target_node = node
                break
        else: 
            self.target_node = PathfindNode(self.player_map_pos) # make sure the target position is a node even if it's not traversable
            self.nodes.append(self.target_node)
    
    def pathfind_calculate(self) -> None:
        """pathfinds to the player by calculating node distances, moving towards the player"""
        pathfind_node = self.current_node # current node the pathfinder is on
        calculated_nodes = [] # holds a list of all nodes calculated but not visited

        while 1: # continue until pathfinding is complete
            pathfind_node.visited = True
            # GET NODES NEXT TO CURRENT ONE
            up = pathfind_node.pos - Vector2(0,1)
            down = pathfind_node.pos + Vector2(0,1)
            left = pathfind_node.pos - Vector2(1,0)
            right = pathfind_node.pos + Vector2(1,0)
            neighbours = [up, down, left, right]
        
            for neighbour in neighbours: # check+update neighbours if the neighbours get closer to the target
                # linear search get the node of the neighbour
                for node in self.nodes:
                    if node.pos == neighbour:
                        neighbour_node = node
                        break
                else: continue # neighbour isn't traversable (out of map/obstacle)

                if neighbour_node.visited: continue # don't recalculate visited nodes
                # add neighbour to calculated nodes
                if neighbour_node not in calculated_nodes: calculated_nodes.append(neighbour_node)

                new_distance = pathfind_node.distance_from_start + 1 # new distance is 1 more than the previous node
                new_total = neighbour_node.heuristic + new_distance  # add heuristic for total distance
                if new_total < neighbour_node.total_distance: # make sure this is the most optimal path
                    neighbour_node.distance_from_start = new_distance
                    neighbour_node.total_distance = new_total
                    neighbour_node.previous_node = pathfind_node
            
            # GET THE CLOSEST NODE FROM TARGET TO VISIT NEXT
            min_node_distance = float("inf") 
            min_node = None
            for node in calculated_nodes: # linear search to find the closest next node
                if node.total_distance < min_node_distance: # current closest path searched
                    min_node_distance = node.total_distance
                    min_node = node
                # tie break if distances are equal
                elif node.total_distance == min_node_distance and min_node_distance != float("inf"):
                    if node.heuristic < min_node.heuristic:
                        min_node = node
                        
            # ALL POSSIBLE NODES VISITED (AND NO TARGET FOUND)
            if min_node == None: 
                # GET VISITED NODE WITH SMALLEST HEURISTIC  
                min_heuristic = float("inf")
                min_heuristic_node = None
                for node in self.nodes: # linear search to find visited node with smallest heurstic
                    if not node.visited: continue
                    if node.heuristic < min_heuristic:
                        min_heuristic = node.heuristic
                        min_heuristic_node = node
                # make new target
                if min_heuristic_node != None: self.target_node = min_heuristic_node
                break # pathfinding done - get path to new target
            
            if min_node == self.target_node: break # finish when reached the target

            pathfind_node = min_node # go to next node
            calculated_nodes.remove(min_node) # remove from calculated as it's going to be visted
    
    def get_path(self, current_end: PathfindNode) -> list:
        """recursively goes back through previous nodes until it reaches the start\n
        returns the shortest path to the start node"""
        previous = current_end.previous_node
        if previous == None: return [current_end.pos] # previous is the start node
        else: return [current_end.pos] + self.get_path(previous) # add the next nodes

    def update_current_path_step(self) -> None:
        """gets the node in the path which the enemy should be travelling to"""
        if self.current_path_step == 0: return
        if self.pos.distance_to(self.current_path_pos) <= settings.ENEMY_NEXT_STEP_DISTANCE:
            self.current_path_step -= 1
            # GET CENTRE OF MAP PIECE, NOT TOPLEFT
            current_rect = pygame.Rect(self.path[self.current_path_step] * settings.PIECE_SIZE, 
                              (settings.PIECE_SIZE, settings.PIECE_SIZE))
            current = Vector2(current_rect.center) 
            next_rect = pygame.Rect(self.path[self.current_path_step+1] * settings.PIECE_SIZE, 
                              (settings.PIECE_SIZE, settings.PIECE_SIZE))
            next = Vector2(next_rect.center) 
            self.current_path_pos = (current+next)/2 # get midpoint between next 2 nodes

            self.speed = settings.ENEMY_SLOW_SPEED # slow down to position to the next step
            self.update_current_path_step()
    
    def adjust_angle(self) -> None:
        """changes the angle of the enemy to try to point at the current path step"""
        # calculate angle between enemy and player
        target_angle = math.atan2(self.current_path_pos.x-self.pos.x, self.current_path_pos.y-self.pos.y)
        target_angle = target_angle*(180/math.pi) + 180

        angle_diff = target_angle - self.angle # how much the current angle needs to change
        if angle_diff > 180: 
            angle_diff -= 360 # take shorter clockwise angle
        elif angle_diff < -180:
            angle_diff += 360 # take shorter anticlockwise angle
        if -1 < angle_diff < 1:
            self.speed = self.max_speed # get back to full speed if pointing correct

        # change in angle is greater than the maximum change in angle per frame
        if abs(angle_diff) > settings.BOAT_MAX_ANGLE_SPEED * 1/tools.get_fps():
            self.angle += (angle_diff/abs(angle_diff)) * settings.BOAT_MAX_ANGLE_SPEED * 1/tools.get_fps()
        else:
            self.angle = target_angle
    
    def try_shoot(self) -> None:
        """enemy tries to shoot at player"""
        self.aim_cannon()
        self.cannons[0].update()
        self.make_main_boat_image() # remake image as cannon has changed angle

        if self.shoot_timer > 0: # timer is running
            self.shoot_timer -= 1/tools.get_fps()
            self.shoot_timer = max(self.shoot_timer, 0) # limit minimum
        
        if self.shoot_timer == 0: # timer ended
            self.cannons[0].shoot()

            # reset timer
            self.shoot_timer = random.uniform(settings.ENEMY_MIN_SHOOT_TIME, settings.ENEMY_MAX_SHOOT_TIME) 
    
    def aim_cannon(self) -> None:
        """aim cannon at player"""
        player_pos = settings.current_run.player_boat.pos # vector of player's position
        cannon_pos = self.pos - (self.cannons[0].centre_offset.rotate(-self.angle)) # vector of cannon position

        dy = player_pos.y-cannon_pos.y # difference in y
        dx = player_pos.x-cannon_pos.x # difference in x

        # angle between cannon and player
        angle = math.atan2(dy, dx) * (180/math.pi)
        relative_angle = 270 - angle - self.angle # adjust relative angle
        
        # make sure 0 <= relative_angle <= 360
        if relative_angle > 360: relative_angle -= 360
        if relative_angle < 0: relative_angle += 360

        self.cannons[0].relative_angle = relative_angle
    
    def hit(self, damage: float) -> None:
        """enemy boat takes damage"""
        self.hp -= damage
        self.hit_sound.play()

        if self.hp <= 0:
            self.die()
    
    def die(self) -> None:
        """what happens when an enemy dies"""
        settings.current_run.kills += 1                           # increase total kills
        settings.current_run.enemy_spawner.wave_dead_enemies += 1 # increasae wave kills

        self.drop_gold()
        self.give_hp()

        self.kill() # remove enemy from all groups
    
    def drop_gold(self) -> None:
        """enemy tries to drop gold"""
        if random.randint(1,100) <= settings.ENEMY_GOLD_CHANCE: 
            # give gold
            settings.current_run.gold += random.randint(settings.MIN_ENEMY_GOLD_AMOUNT, settings.MAX_ENEMY_GOLD_AMOUNT)
    
    def give_hp(self) -> None:
        """attempts to give player hp"""
        if random.randint(1,100) <= settings.ENEMY_HP_CHANCE:
            settings.current_run.player_boat.hp += settings.ENEMY_HP_REGEN # give hp
            # limit maximum hp
            settings.current_run.player_boat.hp = min(settings.current_run.player_boat.hp, settings.GAME.player_stats.hp)
    
    def check_despawn(self) -> None:
        """despawns the enemy if it's too far away"""
        if self.pos.distance_to(settings.current_run.player_boat.pos) >= settings.ENEMY_DESPAWN_DISTANCE:
            self.kill() # remove enemy from all groups
            # decrease spawned enemies so a new one will spawn
            settings.current_run.enemy_spawner.wave_spawned_enemies -= 1