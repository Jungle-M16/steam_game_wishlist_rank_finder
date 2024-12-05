# Steam Game Wishlist Rank Finder 🚀

### 🎮 Automate the search for Steam's most popular games!

No more scrolling through pages on Steam, 50 games at a time, just to find out where your favorite game ranks. **This script does all the heavy lifting for you!** 🔥

---

## 🌟 Features

- **Automated Ranking**: Fetches and displays a game's rank from Steam's wishlist data.  
- **Time Saver**: Forget about the tedious manual search through endless lists.  
- **Local Caching**: Saves results locally for faster future queries.  
  - If the cache is corrupted or deleted, the script automatically refetches the data.  
- **Plug-and-Play Simplicity**: Just run it.  

---

## 🛠️ How It Works

1. Fetches the total list of games ranked by popularity on Steam.
2. Stores the data in a local file to reduce redundant API calls.
3. Checks cache validity:
   - If **cache is invalid**, fetches updated data.
   - If **cache is valid**, queries the local file instead.
4. Displays the rank of your desired game in seconds! ⚡

---

## 📦 Installation

### Prerequisites
- Python 3.x+
- Internet connection

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/steam_game_wishlist_rank_finder.git
   cd steam_game_wishlist_rank_finder
   ```
2. Run the script:
   ```bash
   python rank_finder.py
   ```

---

## 🖼️ Example Usage

```bash
Enter the game name: Cyberpunk 2077
Fetching data...
🎉 'Cyberpunk 2077' is ranked #7 on Steam's wishlist! 🚀 (However Cyberpunk is no longer in the popular wishlist)
```

For subsequent runs, results are fetched from the local cache for instant feedback.  

---

## 🔒 Caching & Validation

The script stores data in `game_list_cache.json`. It:
- **Evicts corrupted or outdated files**: Ensures accurate results.  
- **Avoids redundant fetching**: Reduces data usage and speeds up responses.  

---

## 🤝 Contributions

Want to make this better? Fork the repo, create a new branch, and submit a pull request. All contributions are welcome! 🎉  

---

## 🔧 Support

Having issues? Create an [issue](https://github.com/jungle-m16/steam_game_wishlist_rank_finder/issues), and we'll help you out!

---

## ⚖️ License

This project is licensed under the Unlicense. See the `LICENSE` file for details.

---

Happy gaming! 🎮✨
