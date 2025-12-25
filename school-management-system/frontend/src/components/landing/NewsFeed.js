import React, { useState } from 'react';

const NewsFeed = () => {
    const [news] = useState([
        { id: 1, title: 'School Reopening', content: 'Our school will reopen on September 1st.' },
        { id: 2, title: 'Science Fair', content: 'Join us for the annual science fair on October 15th.' },
        { id: 3, title: 'Sports Day', content: 'Sports Day will be held on November 10th.' },
    ]);

    return (
        <section id="news-feed">
            <div>
                <h2>Latest News</h2>
                <ul>
                    {news.map((item) => (
                        <li key={item.id}>
                            <h3>{item.title}</h3>
                            <p>{item.content}</p>
                        </li>
                    ))}
                </ul>
            </div>
        </section>
    );
};

export default NewsFeed;
