-- my Game Env
local gameEnvMy = {}

local t = {0,1}

function gameEnvMy.getActions()
	return t
end

local debug = false
local MAXSTATE = 15 --self.state_dim
local itr  = 1
local stp  = 0

function gameEnvMy:step(action,training,new)

   local screen = torch.FloatTensor(1,MAXSTATE):fill(0)
   local reward = 0 
   local terminal = false
   local terminal_t
   
   if (new == true) then 
     stp = 0
     itr = 1
     reward = 0
     terminal = false
      
           -- update state  
     screen[1][itr] = 1
   else
     -- preform action 
     stp = stp + 1
     
     
     --right
     if action == 0 then
        itr = itr + 1
        --block
        if(itr>MAXSTATE) then itr = MAXSTATE end
     --left   
     elseif action == 1 then 
        itr = itr - 1
        --blcok
        if itr < 1 then itr = 1 end
     end
     
        -- update state 
            
     screen[1][itr] = 1

  
     
     -- calculate reward
     if itr == MAXSTATE then
      reward = 1
     else
      reward = 0
     end       
     
     -- is terminal?
     if (stp == MAXSTATE + 9) then 
      terminal = true
     else
      terminal = false
     end  

   end
   
   if action==0 then
      act_str = "right"
   else
      act_str = "left" 
   end  
   
   --print("s:"..itr..", a:"..act_str..",r:"..reward..',t:'..tostring(terminal))
   

   return screen , reward, terminal
end 

  
function dataToTensor(data)
  
  local screen = torch.FloatTensor(8):fill(0);
  

  local k = 0
  screen:apply(function ()
                       k = k+1
                       return tonumber(data[k])
                       end)
  
  return screen
end


function gameEnvMy.getState()
  if debug then print("getState") end
  return gameEnvMy:step(99,false,true)
end


function gameEnvMy.newGame()
  if debug then print("newGame") end
  return gameEnvMy:step(99,false,true)
end

function gameEnvMy.nextRandomGame()
  if debug then print("nextRandomGame") end 
  return gameEnvMy:step(99,false,true)
end

function split(s, delimiter)
    if(s==nil) then return;end;
    result = {};
    for match in (s..delimiter):gmatch("(.-)"..delimiter) do
        table.insert(result, match);
    end
    return result;
end



return gameEnvMy
