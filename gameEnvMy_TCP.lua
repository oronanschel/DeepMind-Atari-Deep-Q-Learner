-- my Game Env
local gameEnvMy = {};

-- Connect and listen to local socket on port 1234
local socket = require ("socket");
-- create a TCP socket and bind it to the local host, at any port
local server = socket.try(socket.bind("*", 46329))
-- find out which port the OS chose for us
local ip, port = server:getsockname()
-- print a message informing what's up
print("Please telnet to localhost on port " .. port)

---[[
local client = server:accept()
print("client accepted")
client:settimeout(20)
--]]

function gameEnvMy.getActions()
	local t = {0,1,3,4};
	return t;
end


function gameEnvMy:step(action,training)

  local screen
   --send action
   local eval_time_step = sys.clock(); 
   msg = "action:"..tostring(action)..":0";
   client:send(msg)
   
   -- recive reward,terminal
   local reward = 0 
   local terminal = false
   local data, err = client:receive()
   --print("1Step Time:-0.01") 

   --print("1Step Time:"..(sys.clock()-eval_time_step)) 
    
   
   if not err then
      local msg_parts = split(data,",");
      
      reward = split(msg_parts[1],":")
      reward = tonumber(reward[2])
      --print(reward)      
      local terminal_t  = split(msg_parts[2],":")
      terminal_t    = tonumber(terminal_t[2])
      if(terminal_t==1) then
        terminal = true;       
      else
        terminal = false;
      end 
   
   else   
      print(err)
   end
   
   local eval_time_step2 = sys.clock(); 

   -- recive screen
   data, err = client:receive(30000)
   if not err then
      screen = dataToTensor(data)
   else   
      print(err)
   end
   --print("1Step Time:"..(sys.clock()-eval_time_step2)) 

  
   return screen , reward, terminal
end 

  
function dataToTensor(data)
  
  local height = 100;
  local width = 100;
  local screen = torch.FloatTensor(1,3,100,100):fill(0);
  

  local k = 0
  screen[1][1]:apply(function ()
                       k = k+1
                       return string.byte(data,k)/255   
                       end)
  screen[1][2]:apply(function ()
                       k = k+1
                       return string.byte(data,k)/255   
                       end)
  screen[1][3]:apply(function ()
                       k = k+1
                       return string.byte(data,k)/255   
                       end)                                              
  
  
  return screen
end


function gameEnvMy.getState()
  --print("GetState")
  return gameEnvMy.step(-9)
end


function gameEnvMy.newGame()
  --print("newGame")
  return gameEnvMy.step(-9)
end

function gameEnvMy.nextRandomGame()
  --print("nextRandomGame")
  return gameEnvMy.step(-9)
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
