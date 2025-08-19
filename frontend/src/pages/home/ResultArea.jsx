import React, { useState, useEffect } from 'react';
import "./styles/ResultArea.css";
import FeedbackArea from "./FeedbackArea";

const tmp_sources = [
    {
        "link": "https://www.google.com/search?tbs=simg:CAESbAnG5yuDXzfhihphCxCo1NgEGgIIQgwLELCMpwgaOgo4CAQSFIsypCStLIo7iy_1EB78J7hrtG4UxGhq-RBfFE6HAee0UirMEq_1TJiYJsm0KOr377EiAFMAQMCxCOrv4IGgoKCAgBEgSEmJxlDA&q=elon+musk+&tbm=isch&source=iu&ictx=1&vet=1&fir=CwhZnfDrCaGq3M%252CpQ8CiBj7EMCuvM%252C_%253BvEqnJBqHUctRIM%252CoMUpyI-ZeRd-gM%252C_%253BAJuAbVc44M02AM%252CBz8QIIiY6_V1cM%252C_%253BlH_3ebyJ-6MlLM%252Cpe_xDXIe-__cAM%252C_%253B2IaZF8xqoJssYM%252CdGMKKoCgxL07VM%252C_%253BrRwtU5qRYKN7fM%252CSdlIQkKejjjMPM%252C_%253Bwb8vdHzrs9Ug9M%252CCGJdHrib_cQRIM%252C_%253B3zXyTtWAF1furM%252C0fZr_NLvm8byIM%252C_%253BO09Ej_IqKb6lVM%252CUiGIJK5_gM_1tM%252C_%253BwZpCUrWvV_JglM%252CedYq47OXRNeldM%252C_%253BBBgebJtC_Vl9bM%252CQokyu1qJc9NYaM%252C_%253BipdRYUyrgqMU_M%252CEnCGj_EqjYbpUM%252C_%253B7jxhk24ZYlaC4M%252CmpmcKcsjhk1K3M%252C_%253B0xCj52CM2-PKmM%252CKC_njVjWW0vNPM%252C_%253Bd7ypz2C2vFYDkM%252CGu20SGcxyeEBdM%252C_%253BKsbsN5fuCGFYfM%252CNPSKSqZwF0YOiM%252C_%253BLQQ1KmxpxXywOM%252Cfhucvbrvbdk0kM%252C_%253BX3iL5iBxFNzhMM%252Co812OY6x0QWLQM%252C_%253BJkiKSJWujCi0hM%252C6pYdtNNMKugPhM%252C_%253B2GucjFoPKr01VM%252CU8Ck88w_-9bB2M%252C_%253BxZIhoqd5Lh1sVM%252CSvicoCADoQJWWM%252C_%253BYDSzrvbBYdFFiM%252CyQ9zhLXOEjocfM%252C_&usg=AI4_-kSlHsIUz1e9KT5cycv6NQBqUyx78A&sa=X&ved=2ahUKEwiX09qe0Lj2AhWFRzABHXLCDtgQ9QF6BAgIEAE#imgrc=CwhZnfDrCaGq3M",
        "source": "https://nypost.com/2022/04/04/elon-musk-buys-9-stake-in-twitter-days-after-criticizing-it/",
        "thumbnail": "https://serpapi.com/searches/630e1f0b6066d937c327f955/images/fda37291375b9b601faf0f3927ab9dc42acb3f196cad54153aa132eae7bae086.jpeg",
        "original": "https://nypost.com/wp-content/uploads/sites/2/2022/04/elon-musk-76.jpg",
        "title": "Elon Musk buys 9% stake in Twitter — days after criticizing it Elon Musk buys 9% stake in Twitter — days after criticizing it Elon Musk buys 9% stake in Twitter — days after criticizing it Elon Musk buys 9% stake in Twitter — days after criticizing it"
    },
    {
        "link": "https://www.google.com/search?tbs=simg:CAESbAnG5yuDXzfhihphCxCo1NgEGgIIQgwLELCMpwgaOgo4CAQSFIsypCStLIo7iy_1EB78J7hrtG4UxGhq-RBfFE6HAee0UirMEq_1TJiYJsm0KOr377EiAFMAQMCxCOrv4IGgoKCAgBEgSEmJxlDA&q=elon+musk+&tbm=isch&source=iu&ictx=1&vet=1&fir=CwhZnfDrCaGq3M%252CpQ8CiBj7EMCuvM%252C_%253BvEqnJBqHUctRIM%252CoMUpyI-ZeRd-gM%252C_%253BAJuAbVc44M02AM%252CBz8QIIiY6_V1cM%252C_%253BlH_3ebyJ-6MlLM%252Cpe_xDXIe-__cAM%252C_%253B2IaZF8xqoJssYM%252CdGMKKoCgxL07VM%252C_%253BrRwtU5qRYKN7fM%252CSdlIQkKejjjMPM%252C_%253Bwb8vdHzrs9Ug9M%252CCGJdHrib_cQRIM%252C_%253B3zXyTtWAF1furM%252C0fZr_NLvm8byIM%252C_%253BO09Ej_IqKb6lVM%252CUiGIJK5_gM_1tM%252C_%253BwZpCUrWvV_JglM%252CedYq47OXRNeldM%252C_%253BBBgebJtC_Vl9bM%252CQokyu1qJc9NYaM%252C_%253BipdRYUyrgqMU_M%252CEnCGj_EqjYbpUM%252C_%253B7jxhk24ZYlaC4M%252CmpmcKcsjhk1K3M%252C_%253B0xCj52CM2-PKmM%252CKC_njVjWW0vNPM%252C_%253Bd7ypz2C2vFYDkM%252CGu20SGcxyeEBdM%252C_%253BKsbsN5fuCGFYfM%252CNPSKSqZwF0YOiM%252C_%253BLQQ1KmxpxXywOM%252Cfhucvbrvbdk0kM%252C_%253BX3iL5iBxFNzhMM%252Co812OY6x0QWLQM%252C_%253BJkiKSJWujCi0hM%252C6pYdtNNMKugPhM%252C_%253B2GucjFoPKr01VM%252CU8Ck88w_-9bB2M%252C_%253BxZIhoqd5Lh1sVM%252CSvicoCADoQJWWM%252C_%253BYDSzrvbBYdFFiM%252CyQ9zhLXOEjocfM%252C_&usg=AI4_-kSlHsIUz1e9KT5cycv6NQBqUyx78A&sa=X&ved=2ahUKEwiX09qe0Lj2AhWFRzABHXLCDtgQ9QF6BAgfEAE#imgrc=vEqnJBqHUctRIM",
        "source": "https://www.bloomberg.com/news/newsletters/2022-04-12/an-elon-musk-twitter-takeover-would-follow-these-steps",
        "thumbnail": "https://serpapi.com/searches/630e1f0b6066d937c327f955/images/fda37291375b9b608cf3228280d17073f414474446c2cdc15aefeba9cae05ed6.jpeg",
        "original": "https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iWqMrh7UfZ50/v1/1200x-1.jpg",
        "title": "An Elon Musk Twitter Takeover Would Follow These Steps ..."
    },
    {
        "link": "https://www.google.com/search?tbs=simg:CAESbAnG5yuDXzfhihphCxCo1NgEGgIIQgwLELCMpwgaOgo4CAQSFIsypCStLIo7iy_1EB78J7hrtG4UxGhq-RBfFE6HAee0UirMEq_1TJiYJsm0KOr377EiAFMAQMCxCOrv4IGgoKCAgBEgSEmJxlDA&q=elon+musk+&tbm=isch&source=iu&ictx=1&vet=1&fir=CwhZnfDrCaGq3M%252CpQ8CiBj7EMCuvM%252C_%253BvEqnJBqHUctRIM%252CoMUpyI-ZeRd-gM%252C_%253BAJuAbVc44M02AM%252CBz8QIIiY6_V1cM%252C_%253BlH_3ebyJ-6MlLM%252Cpe_xDXIe-__cAM%252C_%253B2IaZF8xqoJssYM%252CdGMKKoCgxL07VM%252C_%253BrRwtU5qRYKN7fM%252CSdlIQkKejjjMPM%252C_%253Bwb8vdHzrs9Ug9M%252CCGJdHrib_cQRIM%252C_%253B3zXyTtWAF1furM%252C0fZr_NLvm8byIM%252C_%253BO09Ej_IqKb6lVM%252CUiGIJK5_gM_1tM%252C_%253BwZpCUrWvV_JglM%252CedYq47OXRNeldM%252C_%253BBBgebJtC_Vl9bM%252CQokyu1qJc9NYaM%252C_%253BipdRYUyrgqMU_M%252CEnCGj_EqjYbpUM%252C_%253B7jxhk24ZYlaC4M%252CmpmcKcsjhk1K3M%252C_%253B0xCj52CM2-PKmM%252CKC_njVjWW0vNPM%252C_%253Bd7ypz2C2vFYDkM%252CGu20SGcxyeEBdM%252C_%253BKsbsN5fuCGFYfM%252CNPSKSqZwF0YOiM%252C_%253BLQQ1KmxpxXywOM%252Cfhucvbrvbdk0kM%252C_%253BX3iL5iBxFNzhMM%252Co812OY6x0QWLQM%252C_%253BJkiKSJWujCi0hM%252C6pYdtNNMKugPhM%252C_%253B2GucjFoPKr01VM%252CU8Ck88w_-9bB2M%252C_%253BxZIhoqd5Lh1sVM%252CSvicoCADoQJWWM%252C_%253BYDSzrvbBYdFFiM%252CyQ9zhLXOEjocfM%252C_&usg=AI4_-kSlHsIUz1e9KT5cycv6NQBqUyx78A&sa=X&ved=2ahUKEwiX09qe0Lj2AhWFRzABHXLCDtgQ9QF6BAgKEAE#imgrc=AJuAbVc44M02AM",
        "source": "https://www.washingtonpost.com/technology/2022/04/25/twitter-elon-musk-deal/",
        " ": "https://serpapi.com/searches/630e1f0b6066d937c327f955/images/fda37291375b9b6045a1dd41ef10e6fecd013afc3982cac6b787b72ed50b906b.jpeg",
        "original": "https://arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/FULLSSGBUEI6ZNO7D65GDJTMOU.jpg",
        "title": "Elon Musk reaches deal to buy Twitter - The Washington Post"
    },
    {
        "link": "https://www.google.com/search?tbs=simg:CAESbAnG5yuDXzfhihphCxCo1NgEGgIIQgwLELCMpwgaOgo4CAQSFIsypCStLIo7iy_1EB78J7hrtG4UxGhq-RBfFE6HAee0UirMEq_1TJiYJsm0KOr377EiAFMAQMCxCOrv4IGgoKCAgBEgSEmJxlDA&q=elon+musk+&tbm=isch&source=iu&ictx=1&vet=1&fir=CwhZnfDrCaGq3M%252CpQ8CiBj7EMCuvM%252C_%253BvEqnJBqHUctRIM%252CoMUpyI-ZeRd-gM%252C_%253BAJuAbVc44M02AM%252CBz8QIIiY6_V1cM%252C_%253BlH_3ebyJ-6MlLM%252Cpe_xDXIe-__cAM%252C_%253B2IaZF8xqoJssYM%252CdGMKKoCgxL07VM%252C_%253BrRwtU5qRYKN7fM%252CSdlIQkKejjjMPM%252C_%253Bwb8vdHzrs9Ug9M%252CCGJdHrib_cQRIM%252C_%253B3zXyTtWAF1furM%252C0fZr_NLvm8byIM%252C_%253BO09Ej_IqKb6lVM%252CUiGIJK5_gM_1tM%252C_%253BwZpCUrWvV_JglM%252CedYq47OXRNeldM%252C_%253BBBgebJtC_Vl9bM%252CQokyu1qJc9NYaM%252C_%253BipdRYUyrgqMU_M%252CEnCGj_EqjYbpUM%252C_%253B7jxhk24ZYlaC4M%252CmpmcKcsjhk1K3M%252C_%253B0xCj52CM2-PKmM%252CKC_njVjWW0vNPM%252C_%253Bd7ypz2C2vFYDkM%252CGu20SGcxyeEBdM%252C_%253BKsbsN5fuCGFYfM%252CNPSKSqZwF0YOiM%252C_%253BLQQ1KmxpxXywOM%252Cfhucvbrvbdk0kM%252C_%253BX3iL5iBxFNzhMM%252Co812OY6x0QWLQM%252C_%253BJkiKSJWujCi0hM%252C6pYdtNNMKugPhM%252C_%253B2GucjFoPKr01VM%252CU8Ck88w_-9bB2M%252C_%253BxZIhoqd5Lh1sVM%252CSvicoCADoQJWWM%252C_%253BYDSzrvbBYdFFiM%252CyQ9zhLXOEjocfM%252C_&usg=AI4_-kSlHsIUz1e9KT5cycv6NQBqUyx78A&sa=X&ved=2ahUKEwiX09qe0Lj2AhWFRzABHXLCDtgQ9QF6BAgKEAE#imgrc=AJuAbVc44M02AM",
        "source": "https://www.washingtonpost.com/technology/2022/04/25/twitter-elon-musk-deal/",
        " ": "https://serpapi.com/searches/630e1f0b6066d937c327f955/images/fda37291375b9b6045a1dd41ef10e6fecd013afc3982cac6b787b72ed50b906b.jpeg",
        "original": "https://arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/FULLSSGBUEI6ZNO7D65GDJTMOU.jpg",
        "title": "Elon Musk reaches deal to buy Twitter - The Washington Post"
    },
    {
        "link": "https://www.google.com/search?tbs=simg:CAESbAnG5yuDXzfhihphCxCo1NgEGgIIQgwLELCMpwgaOgo4CAQSFIsypCStLIo7iy_1EB78J7hrtG4UxGhq-RBfFE6HAee0UirMEq_1TJiYJsm0KOr377EiAFMAQMCxCOrv4IGgoKCAgBEgSEmJxlDA&q=elon+musk+&tbm=isch&source=iu&ictx=1&vet=1&fir=CwhZnfDrCaGq3M%252CpQ8CiBj7EMCuvM%252C_%253BvEqnJBqHUctRIM%252CoMUpyI-ZeRd-gM%252C_%253BAJuAbVc44M02AM%252CBz8QIIiY6_V1cM%252C_%253BlH_3ebyJ-6MlLM%252Cpe_xDXIe-__cAM%252C_%253B2IaZF8xqoJssYM%252CdGMKKoCgxL07VM%252C_%253BrRwtU5qRYKN7fM%252CSdlIQkKejjjMPM%252C_%253Bwb8vdHzrs9Ug9M%252CCGJdHrib_cQRIM%252C_%253B3zXyTtWAF1furM%252C0fZr_NLvm8byIM%252C_%253BO09Ej_IqKb6lVM%252CUiGIJK5_gM_1tM%252C_%253BwZpCUrWvV_JglM%252CedYq47OXRNeldM%252C_%253BBBgebJtC_Vl9bM%252CQokyu1qJc9NYaM%252C_%253BipdRYUyrgqMU_M%252CEnCGj_EqjYbpUM%252C_%253B7jxhk24ZYlaC4M%252CmpmcKcsjhk1K3M%252C_%253B0xCj52CM2-PKmM%252CKC_njVjWW0vNPM%252C_%253Bd7ypz2C2vFYDkM%252CGu20SGcxyeEBdM%252C_%253BKsbsN5fuCGFYfM%252CNPSKSqZwF0YOiM%252C_%253BLQQ1KmxpxXywOM%252Cfhucvbrvbdk0kM%252C_%253BX3iL5iBxFNzhMM%252Co812OY6x0QWLQM%252C_%253BJkiKSJWujCi0hM%252C6pYdtNNMKugPhM%252C_%253B2GucjFoPKr01VM%252CU8Ck88w_-9bB2M%252C_%253BxZIhoqd5Lh1sVM%252CSvicoCADoQJWWM%252C_%253BYDSzrvbBYdFFiM%252CyQ9zhLXOEjocfM%252C_&usg=AI4_-kSlHsIUz1e9KT5cycv6NQBqUyx78A&sa=X&ved=2ahUKEwiX09qe0Lj2AhWFRzABHXLCDtgQ9QF6BAgKEAE#imgrc=AJuAbVc44M02AM",
        "source": "https://www.washingtonpost.com/technology/2022/04/25/twitter-elon-musk-deal/",
        " ": "https://serpapi.com/searches/630e1f0b6066d937c327f955/images/fda37291375b9b6045a1dd41ef10e6fecd013afc3982cac6b787b72ed50b906b.jpeg",
        "original": "https://arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/FULLSSGBUEI6ZNO7D65GDJTMOU.jpg",
        "title": "Elon Musk reaches deal to buy Twitter - The Washington Post"
    }
  ];

const LoadingMessage = () => <div className="loading-message">Loading...</div>;
const ErrorMessage = ({ message }) => <p className="error-message">Error: {message}</p>;
const ImageDisplay = ({ src, alt }) => <img src={src} alt={alt} className="image-display" />;
const PredictionResult = ({ fileName, category, accuracy, confidence }) => (
    <div className="prediction-result">
        <div className="prediction-secion">
            <h3>File Name</h3>
            <p>{fileName}</p>
        </div>
        <div className="prediction-secion longer-prediction-secion">
            <h3>Predicted Category</h3>
            <p>{category}</p>
        </div>
        <div className="prediction-secion">
            <h3>Result Accuracy</h3>
            <p>{accuracy}%</p>
        </div>
        <div className="prediction-secion longer-prediction-secion">
            <h3>Confidence Interval</h3>
            <p>[{confidence[0]}, {confidence[1]}]</p>
        </div>
    </div>
);

let vis = {};

function ResultArea({ img, id, fileName }) {
    if (id in vis) {
        return vis[id];
    }

    const [result, setResult] = useState({
        content: 'Loading...',
        heatmapImage: '',
        predictions: [],
        loading: true,
        error: null,
    });
    const [feedbackKey, setFeedbackKey] = useState(0);

    useEffect(() => {
        if (!img) {
            setResult({ ...result, content: 'No image uploaded.', loading: false });
            return;
        }
        setResult({ content: 'Loading...', heatmapImage: '', predictions: [], loading: true, error: null });
        const uploadedImage = img.split(',')[1];
        fetchPredictions(uploadedImage);
    }, [img]);

    const fetchPredictions = (image) => {
        const url = 'https://artifa.apps.austinjiang.com/detect';
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({ image }),
        };

        fetch(url, options)
            .then(response => response.json())
            .then(data => {
                handleResponse(data);
                setFeedbackKey(prevKey => prevKey + 1);
            })
            .catch(error => {
                console.error('Fetch error:', error);
                setResult({ ...result, content: `Failed to fetch data. ${error.toString()}`, loading: false });
            });
    };

    const handleResponse = (data) => {
        if (data.error) {
            setResult({ ...result, error: data.error, loading: false });
        } else {
            const heatmapImage = `data:image/png;base64,${data.heatmap}`;
            setResult({
                ...result,
                content: JSON.stringify(data, null, 2),
                heatmapImage,
                predictions: data.predictions,
                sources: data.sources,
                loading: false,
            });
        }
    };

    const calculatePredictions = () => {
        const adjustedPredictions = result.predictions.map(prediction => Math.round(prediction * 100));
        const maxPrediction = Math.max(...adjustedPredictions);
        const categoryIndex = adjustedPredictions.indexOf(maxPrediction);
        const category = ["Created By AI", "Created By Human"][categoryIndex];
        return {
            category,
            accuracy: maxPrediction,
            confidence: result.predictions,
        };
    };

    if (result.loading) return <LoadingMessage />;
    if (result.error) return <ErrorMessage message={result.error} />;

    const { category, accuracy, confidence } = calculatePredictions();

    const sources = result.sources;//tmp_sources;

    vis[id] = (
        <div className="result-area">
            <div className="title-feedback-container">
                <h2>Result Summary</h2>
                <FeedbackArea key={feedbackKey} />
            </div>
            <div className="result-content">
                <div className="card original-image-section">
                    <h3>Original Image</h3>
                    <ImageDisplay src={img} alt="Original Image" />
                </div>
                <div className="text-area card">
                    <PredictionResult fileName={fileName} category={category} accuracy={accuracy} confidence={confidence} />
                </div>
                <div className="card heatmap-section">
                    <h3>Heatmap of Contribution</h3>
                    <ImageDisplay src={result.heatmapImage} alt="Heatmap" />
                </div>
                <div className="source-area card">
                    <h3>Potential Origins</h3>
                    {
                        0&&sources.length > 0 ? (
                            <div className="sources">
                                {sources.map((source) => (
                                    <div className="source">
                                        <a href={source.source} target="_blank">{source.title}</a>
                                        <img src={source.original} />
                                    </div>
                                ))}
                            </div>
                        ) :
                        (
                            <p>The function is temporarily unavailable as the monthly trial limit has been reached.</p>
                        )
                    }
                </div>
            </div>
        </div>
    );
    return vis[id];
}

export default ResultArea;