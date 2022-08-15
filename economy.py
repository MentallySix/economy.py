import discord
from discord import activity
from discord.ext import commands
import random
import asyncio
names = ['Pablo','Bob','Flowey🌻 :)','Obama','Saleem','Your mom','Kathey','Joshua','Max','Billy','Stacy','Jessica','Ishaan','Andrew Tate','Patrick Batemen','Uncle Roger','Hamza','Elongate Muskrat','Your Step-Sister','Gort','Ovuvuevuevue Enyetuenwuevue Ugbemugbem Osas']
fuiyoh='<a:fuiyoh:998244616434352280>'


async def embeding(ctx,title,description,colourr):
    if colourr == 'red':
        embed = discord.Embed(title=title,description=description,color = discord.Color.red())
    elif colourr == 'green':
        embed = discord.Embed(title=title,description=description,color = discord.Color.green())
    elif colourr == 'blue':
        embed = discord.Embed(title=title,description=description,color = discord.Color.blue())
    elif colourr == 'orange':
        embed = discord.Embed(title=title,description=description,color = discord.Color.orange())
    elif colourr == 'random':
        embed = discord.Embed(title=title,description=description,color= discord.Color.random())
    return embed

async def stringtolist(string):
    if string == None:
        return ''
    else:
        listRes = list(string.split(","))
        return listRes

async def listtostring(listt):
    listt = str(listt)
    listt = listt.replace('[','')
    listt = listt.replace(']','')
    listt = listt.replace("'",'')
    listt = listt.replace(" ",'')
    return listt

async def checking(ctx,member):
    try:
        check = await ctx.bot.db.fetch('SELECT user_id FROM teamwork WHERE user_id = $1', member)
        return True
    except:
        await ctx.send(await embeding(ctx, "**uhhh you forgettin smth**", "Create an account first!", "red"))
        return False    

async def item_stats(ctx,item,STATe):
        info = await ctx.bot.db.fetch(f'SELECT {STATe} FROM item WHERE item = $1',item)
        return info[0][STATe]

async def get_money(ctx,user,balance,profit):
    leader = await ctx.bot.db.fetch('SELECT leader FROM teamwork WHERE user_id = $1',user)
    await ctx.bot.db.execute('UPDATE teamwork SET balance = $1 WHERE user_id = $2',balance+profit,leader[0]['leader'])

async def role_check(ctx,user,role):
    user_role = await ctx.bot.db.fetch('SELECT role FROM teamwork WHERE user_id = $1', user)
    if user_role[0]['role'] != role:
        await ctx.send(embed=await embeding(ctx, '**Uhhh**', f'You need **{role}** role!', 'red'))
        return False

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_prefix(bot,message):
        guild = message.guild.id
        prefix_ = await bot.db.fetch('SELECT prefix FROM server_prefix WHERE guilds_id = $1',guild)
        if prefix_ == []:
            PREFIX = '.'
        else:
            PREFIX = prefix_[0]['prefix']
        global prefix
        prefix = PREFIX
        return PREFIX    

        
    #                                                                                     farming
    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def plant(self,ctx):

        user_stats = await ctx.bot.db.fetch('SELECT * FROM stats WHERE user_id = $1',ctx.author.id)
        user_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',ctx.author.id)
        leader_stats = await ctx.bot.db.fetch('SELECT * FROM stats WHERE user_id = $1',user_info[0]['leader'])
        leader_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',user_info[0]['leader'])
        plant = await stringtolist(user_stats[0]['inventory'])
        newinventory = leader_stats[0]['inventory']
        inventory = await stringtolist(newinventory)

        if 'orchidseed' in plant:
            planted = 'orchid'
        elif 'mangoseed' in plant:
            planted = 'mango'
        elif 'riceseed' in plant:
            planted = 'rice'
        elif 'maniocseed' in plant:
            planted = 'manioc'
        else:
            planted = 'weed'
        planty = planted

        emoji = await ctx.bot.db.fetch('SELECT emoji FROM item WHERE item = $1', planted)

        if 'escavator' in inventory:
            amount = 125
        elif 'mattock' in inventory:
            amount = 50    
        elif 'shovel' in inventory:
            amount = 25     
        else:
            amount = 10

        
        if await checking(ctx,ctx.author.id) == False:pass
        elif await role_check(ctx, ctx.author.id, 'planter') == False:pass
        else:
            i = 0
            if newinventory == None or newinventory == 'None':
                newinventory= (planted+((','+planted)*amount))

            else:
                planted = (','+planted)*amount
                newinventory = (newinventory+planted)
            await ctx.bot.db.execute('UPDATE stats SET inventory = $1 WHERE user_id = $2 ', str(newinventory) , user_info[0]['leader'])
            await ctx.send(embed=await embeding(ctx,None,f"You planted **{amount}x {planty}**{emoji[0]['emoji']} !",'random'))

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def harvest(self,ctx):
        user_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',ctx.author.id)
        leader_stats = await ctx.bot.db.fetch('SELECT * FROM stats WHERE user_id = $1',user_info[0]['leader'])
        leader_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',user_info[0]['leader'])
        inventory = await stringtolist2(leader_stats[0]['inventory'])
        plants = ['weed','rice','manioc','mango','orchid']
        i = 0
        ii = 0 
        harvested = []
        harvestedd = []
        harvest = False
        user_plants = []
        for x in plants:
            if plants[ii] in inventory:
                harvest = True
                user_plants.append(plants[ii])
                break
            else:
                pass
            ii += 1



        if 'truck' in inventory:
            amount = 100
        elif 'trolley' in inventory:
            amount = 50
        elif 'backpack' in inventory:
            amount = 25
        else:
            amount = 10

        if 'katana' in inventory:
            attack = 0
        elif 'chainsaw' in inventory:
            attack = random.randint(5,10)
        elif 'machete' in inventory:
            attack = random.randint(15,20)
        elif 'scissors' in inventory:
            attack = random.randint(20,30)
        else:
            attack = random.randint(40,50)
        totalattk = 0 
        
        if await checking(ctx,ctx.author.id) == False:pass
        elif await role_check(ctx, ctx.author.id, 'harvester') == False: pass
        elif harvest == False: await ctx.send(embed=await embeding(ctx,'**uhhh**','You do not have anything to harvest!','red'))
        else:


            for x in user_plants:
                plant = plants[i]
                count = inventory.count(plant)
                if count < amount:
                    amount = count
                attackk = round((attack/100*count))
                totalattk += attackk
                amountt = amount
                amount = abs(amount-attackk)
                for x in range(amountt):
                    inventory.remove(plant)
                for x in range(amount):
                    inventory.append(plant+'H')
                if count > 0:
                    emoji = await ctx.bot.db.fetch('SELECT emoji FROM item WHERE item = $1',plant)            
                    harvestedd.append(plant)
                    harvested.append(f"**{amount}x** {plant}{emoji[0]['emoji']}")
                i += 1
    
            if totalattk > 0:
                insectattack = f'\n**{totalattk}** of your crops were eaten by insects🦗!' 
            else:
                insectattack = ''

            harvested = await listtostring2(harvested)
            harvested= harvested.replace(',','\n')
            harvested= harvested.replace('[]','xz ')
            await ctx.send(embed=await embeding(ctx,None,f'You harvested\n{harvested}!{insectattack}','green')) 
            await ctx.bot.db.execute('UPDATE stats SET inventory = $1 WHERE user_id = $2',await listtostring(inventory),user_info[0]['leader'])

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def sell(self,ctx,item):
        item = item.lower()
        if await checking(ctx,ctx.author.id) == False:return
        elif await role_check(ctx, ctx.author.id, 'seller') == False:return
        
        user_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',ctx.author.id)
        inventory = await ctx.bot.db.fetch('SELECT * FROM stats WHERE user_id = $1',ctx.author.id)
        leader_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',user_info[0]['leader'])
        inventory = await stringtolist(inventory[0]['inventory'])
        plants = ['weedH','riceH','maniocH','mangoH','orchidH']
        profit = 0
        i = 0
        totalP = 0 

        if item+'H' in plants:
            if 'worldplant' in inventory:
                amount = 125
            elif 'supermarket' in inventory:
                amount = 50
            elif 'cornershop' in inventory:
                amount = 25
            else:
                amount = 10
            count = inventory.count(item+'H')
            
            if count > amount:
                pass
            elif count == 0:
                await ctx.send(embed = await embeding(ctx,'**uhhh**','You do not have anything to sell!','red'))
                return
            elif count < amount:
                amount = count
            

            plantstat = await item_stats(ctx,item+'H','stat')
            minimum = int((80/100)*plantstat)
            earn = ((random.randint(minimum,plantstat))*amount)*leader_info[0]['multiplier']
            for x in range(amount):
                inventory.remove(item+'H')
            
            await ctx.bot.db.execute('UPDATE stats SET inventory = $1 WHERE user_id = $2',await listtostring(inventory),ctx.author.id)
            await get_money(ctx,user_info[0]['leader'],leader_info[0]['balance'],earn)
            await ctx.send(embed= await embeding(ctx,'**Fuiyohhh**',f"You sold **x{amount} {item.capitalize()}**{await item_stats(ctx,item,'emoji')}\n+*{earn}$*",'green'))
    

    #                                                                                    street band
    @commands.command()
    @commands.cooldown(1,25,commands.BucketType.user)
    async def sing(self,ctx):
        name = random.choice(names)
        user = ctx.author.id
        user_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', user)
        leader_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', user_info[0]['leader'])
        inventory = await ctx.bot.db.fetch('SELECT inventory FROM stats WHERE user_id = $1', user)
        try:
            inventory = inventory[0]['inventory']
            if 'autotune' in inventory:
                amount = 65
            elif 'chair' in inventory:
                amount = 55
            elif 'speaker' in inventory:
                amount = 45
            elif 'microphone' in inventory:
                amount = 35
            else:
                amount = 20
        except:
            inventory = ''
            amount = 10
        if await checking(ctx,ctx.author.id) == False:return
        elif await role_check(ctx, ctx.author.id, 'singer') == False:return
        else:
            amount = random.randint(1,amount)
            await get_money(ctx,user,leader_info[0]['balance'],amount)
            await ctx.send(embed= await embeding(ctx,'**Lessgoo**',f'*{name}* gave you **{amount}$** for singing so well🎶!','random'))
        
    @commands.command()
    @commands.cooldown(1,25,commands.BucketType.user)
    async def play(self,ctx):
        name = random.choice(names)
        user = ctx.author.id
        user_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', user)
        leader_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', user_info[0]['leader'])
        inventory = await ctx.bot.db.fetch('SELECT inventory FROM stats WHERE user_id = $1', user)

        try:
            inventory = inventory[0]['inventory']  
            if 'piano' in inventory:
                amount = 75
            elif 'violin' in inventory:
                amount = 65
            elif 'guitar' in inventory:
                amount = 55
            elif 'triangle' in inventory:
                amount = 45
            else:
                amount = 3
        except:
            amount = 20
            inventory = ''
        
      
        if await checking(ctx,ctx.author.id) == False:return
        elif await role_check(ctx, ctx.author.id, 'player') == False:return
        else:
            amount = random.randint(1,amount)
            await get_money(ctx,user,leader_info[0]['balance'],amount)
            await ctx.send(embed= await embeding(ctx,'**Lessgoo**',f'*{name}* gave you **{amount}$** for playing so well🎶!','random'))


    #                                                                   Restaurant
    @commands.command()
    async def menu(self,ctx):
        menubed = discord.Embed(title='᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆Menu᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆᠆',color=discord.Color.random())
        menubed.add_field(name='1.Rice Porridge',value='🍙\n2️⃣\nGet *20$* after each sales!\nID:`porridge`',inline=False)
        menubed.add_field(name='\n2.Fish n Chips',value='🐟 🍟\n1️⃣ 1️⃣\nGet *40$* after each sales!\nID:`fishchip`',inline=False)
        menubed.add_field(name='\n3.Egg Fried Rice',value='🥚 🍙\n1️⃣ 2️⃣\nGet *60$* after each sales!\nID:`eggrice`',inline=False)
        menubed.add_field(name='\n4.Sushi',value='🐟 🍙\n3️⃣ 2️⃣\nGet *80$* after each sales!\nID:`sushi`',inline=False)
        menubed.set_footer(text='.cook <ID>')
        await ctx.send(embed=menubed)

    @commands.command()
    async def ingredients(self,ctx):
        user = ctx.author.id
        if await checking(ctx,user) == False: return
        elif await role_check(ctx,user,'chef') == False: return       
        inventory= await ctx.bot.db.fetch('SELECT inventory FROM stats WHERE user_id = $1',user)
        inventory = inventory[0]['inventory']
        if '' in inventory:
            items = []
            amount = 1
        elif '' in inventory:
            items = []
            amount = 1
        elif '' in inventory:
            items = []
            amount = 1
        elif '' in inventory:
            items = []
            amount = 1        

    @commands.command()
    async def cook(food,self,ctx):
        pass
    
    @commands.command()
    async def serve(self,ctx):
        pass



    @commands.command()
    @commands.cooldown(1,30,commands.BucketType.user)
    async def beg(self,ctx):
        if await checking(ctx,ctx.author.id) == False: return
        user_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', ctx.author.id)
        leader_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',user_info[0]['leader'])
        name = random.choice(names)
        earn = (random.randint(1,20))*leader_info[0]['multiplier']
        await get_money(ctx, user_info[0]['leader'], leader_info[0]['balance'], earn)
        await ctx.send(embed=await embeding(ctx,f'**Lessgoo** ',f'*{name}* gave you **{earn}$**! ','random'))

    @commands.command()
    async def gamble(self,ctx,amount:int):
        user = ctx.author.id
        user_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',user)
        leader_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',user_info[0]['leader'])
        winorloss = ("win" , "loss")
        
        if await checking(ctx,user) == False: pass
        elif amount > 100000:await ctx.send(embed=await embeding(ctx,'**Uhhh**','You cannot gamble more than 100,000$ !','red'))
        elif amount > leader_info[0]['balance']: await ctx.send(embed=await embeding(ctx,'**Uhhh**','You do not have enough money!','red'))
        else:
            winloss = random.choice(winorloss)
            if winloss == ('win'):
                newamount = amount + leader_info[0]['balance']
                await ctx.bot.db.execute('UPDATE teamwork SET balance = $1 WHERE user_id = $2' , newamount , user_info[0]['leader'])
                await ctx.send(embed=await embeding(ctx,'**Lessgoo**',f'You won **{amount}$**!','green'))
            elif winloss == ('loss'):
                newamount = leader_info[0]['balance'] - amount
                await ctx.bot.db.execute('UPDATE teamwork SET balance = $1 WHERE user_id = $2' , newamount , user_info[0]['leader'])
                await ctx.send(embed = await embeding(ctx,'**Rip lmfao**',f'You lost **{amount}$**!','red'))

    @commands.command()
    async def guess(self,ctx,amount:int):
        rounds = 0
        multiplier = 5
        user = ctx.author.id
        user_info = await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1', user)
        leader_info=await ctx.bot.db.fetch('SELECT * FROM teamwork WHERE user_id = $1',user_info[0]['leader'])
        num = random.randint(0,100)
        if await checking(ctx,user) == False: pass
        elif amount > 100000:await ctx.send(embed=await embeding(ctx,'**Uhhh**','You cannot gamble more than 100,000$ !','red'))
        elif amount > leader_info[0]['balance']: await ctx.send(embed=await embeding(ctx,'**Uhhh**','You do not have enough money!','red'))
        else:
            await ctx.send(embed=await embeding(ctx,'Number Generated','A Number Between 1-100 was generated!\nType your guess','random'))
            for x in range(10):
                try:
                    rounds = rounds + 1
                    multiplier = multiplier - 1
                    if rounds == 5:
                        amount = leader_info[0]['balance']-amount
                        await ctx.bot.db.execute('UPDATE teamwork SET balance = $1 WHERE user_id = $2',amount , user_info[0]['leader'])
                        await ctx.send(embed=await embeding(ctx,'**Better Luck Next Time..**',f'You used all your guesses!\nThe number was *{num}*!','random'))
                        break
                    
                    msg = await self.bot.wait_for('message',timeout = 50 , check=lambda message: message.author == ctx.author)

                    try:
                        msg.content = int(msg.content) 
                    except:
                        await ctx.send(embed=await embeding(ctx,'Uhhh','Please type a valid number!','red'))
                        break
                    
            
                    if msg.content == num:
                        amount = amount*multiplier
                        await get_money(ctx,user,leader_info[0]['balance'],amount)
                        await ctx.send(embed= await embeding(ctx,'**Lessgoo**',f'You won **{amount}** ! \n *{rounds}* guesses','green'))
                        break
                    
                    elif msg.content > num:
                        await ctx.send(embed= await embeding(ctx, 'Try Again..', 'Lower', 'random'))
                    
                    elif msg.content < num:
                        await ctx.send(embed= await embeding(ctx, 'Try Again..', 'Higher', 'random'))
                       
                    

                except asyncio.TimeoutError:
                    await ctx.send(embed=await embeding(ctx,'**Uhhh**',"You didn't reply on time!",'red'))
                    break

    @sell.error
    async def sell_error(self,ctx,error):
        embed= await embeding(ctx,'**Uhhh**','What are you selling?','red')
        embed.add_field(name='Example:',value=f'`.sell bathwater`')
        await ctx.send(embed=embed)

    @gamble.error
    async def gamble_error(self,ctx,error):
        embed= await embeding(ctx,'**Uhhh**','How much are you gambling?','red')
        embed.add_field(name='Example:',value=f'`.gamble 420`')
        await ctx.send(embed=embed)

    @guess.error
    async def guess_error(self,ctx,error):
        embed= await embeding(ctx,'**Uhhh**','How much are you gambling?','red')
        embed.add_field(name='Example:',value=f'`.guess 69`')
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(economy(bot))